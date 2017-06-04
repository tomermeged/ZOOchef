# for python 2.7

# Response object:
# Upon receiving a response, Unirest returns the result in the form of an Object.
# This object should always have the same keys for each language regarding to the response details.
#
# Response.code - HTTP Response Status Code (Example 200)
# Response.headers- HTTP Response Headers
# Response.body- Parsed response body where applicable, for example JSON responses are parsed to Objects / Associative Arrays.
# Response.raw_body- Un-parsed response body



from common import *
from recipe_objects import *
from ingredients_DB import *

# def add_to_ing_db(ingredientName, ConvertContainersResponseBody):

	# f_IngredientsDB = file(ProjectPath + FilenameIngredientsDB, 'w')
	# f_IngredientsDB.close()



def get_conversion_from_db(sourceUnit, sourceAmount, ConversionTableIndx):
	DBsourceAmount = ConversionTable[ConversionTableIndx][sourceUnit]
	NormFactor = DBsourceAmount / sourceAmount
	DBTargetAmount = ConversionTable[ConversionTableIndx][TargetUnit]

	return DBTargetAmount * NormFactor

def convert_containers(indx) :
	ingredientName = ingredients[indx]["name"]
	sourceAmount = ingredients[indx]["amount"]
	sourceUnit = ingredients[indx]["unit"]
	debug(ingredientName)
	debug(sourceUnit)
	debug(TargetUnit)
	ConversionTableIndx = 0
	TargetUnitExist = False
	SourceUnitExist = False

	# checking if all necessary conversion data exist in DB
	for ConversionTableIndx in range(0, ConversionTableSize):
		if ConversionTable[ConversionTableIndx]["name"] == ingredientName:
			if sourceUnit in ConversionTable[ConversionTableIndx]:
				SourceUnitExist = True
			if TargetUnit in ConversionTable[ConversionTableIndx]:
				TargetUnitExist = True
			break

	if TargetUnitExist  == True and SourceUnitExist  == True: # exist
		info("get_conversion_from_db")
		return get_conversion_from_db(sourceUnit, sourceAmount, ConversionTableIndx)

	else:
		global GlobalNumUsedServer

		info("using server(" + str(GlobalNumUsedServer) + "): " + WordConvert)
		GlobalNumUsedServer += 1
		ConvertContainersResponse = unirest.get(SpoonacularServer + WordConvert +
													"ingredientName=" + ingredientName +
													"&sourceAmount=" + str(sourceAmount) +
													"&sourceUnit=" + sourceUnit +
													"&targetUnit=" + TargetUnit,
		  headers={
			"X-Mashape-Key": MyMashapeKey,
			"Accept": "application/json"
		  }
		)
		debug(ConvertContainersResponse.body)
		if ConversionTableIndx < ConversionTableSize - 1:
			debug("ingredient exist")
			if TargetUnitExist == True:
				debug("only source unit is missing")
				ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["sourceUnit"]] = ConvertContainersResponse.body["sourceAmount"]
			else:
				debug("target unit is missing --> add entry to dictionary")
				ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["targetUnit"]] = ConvertContainersResponse.body["targetAmount"]
				if SourceUnitExist == False:
					debug("source unit is missing --> add entry to dictionary")
					ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["sourceUnit"]] = ConvertContainersResponse.body["sourceAmount"]
			debug(ConversionTable[ConversionTableIndx])
		else:
			debug("create new dictionary for ingredient --> add both source and target")
			ConvIng = {"name":ingredients[indx]["name"]}
			ConvIng["id"] = ingredients[indx]["id"]
			ConvIng["aisle"] = ingredients[indx]["aisle"]
			ConvIng[ConvertContainersResponse.body["sourceUnit"]] = ConvertContainersResponse.body["sourceAmount"]
			ConvIng[ConvertContainersResponse.body["targetUnit"]] = ConvertContainersResponse.body["targetAmount"]
			ConversionTable.append(ConvIng)

		NewConversionTableSize = len(ConversionTable)
		f_IngredientsDB = file(ProjectPath + FilenameIngredientsDB, 'w')
		f_IngredientsDB.write("ConversionTable = [")
		f_IngredientsDB.write("\n")
		for ConversionTableIndx in range(0, NewConversionTableSize):
			f_IngredientsDB.write(str(ConversionTable[ConversionTableIndx]) + ",")
			f_IngredientsDB.write("\n")
		f_IngredientsDB.write("]" )
		f_IngredientsDB.write("\n")
		f_IngredientsDB.write("ConversionTableSize = len(ConversionTable)" )
		f_IngredientsDB.close()
		return ConvertContainersResponse.body["targetAmount"]
		# example response:
		# {u'sourceUnit': u'cup',
		# u'targetUnit': u'grams',
		# u'sourceAmount': 0.25,
		# u'answer': u'0.25 cup chicken broth translates to 58.75 grams.',
		# u'targetAmount': 58.75,
		# u'type': u'CONVERSION'}


def edit_html_template() :

	global steps
	# files & paths:
	html_template_filename = "html_template\zoo_cheff_templateDraft.htm"
	new_html_recipe_filename = attributes[1]["title"] + "_" + str(attributes[1]["id"]) + ".htm"

	f_html_template = file(ProjectPath + html_template_filename, 'r')
	f_new_html_recipe = file(ProjectPath + new_html_recipe_filename, 'w')

	new_recipe_data = f_html_template.read()

	new_recipe_data = new_recipe_data.replace("recipeName", str(attributes[1]["title"]))
	new_recipe_data = new_recipe_data.replace("sourceURL", str(attributes[0]["sourceUrl"]))

	num_ingredients = len(ingredients)

	for indx in range(0, num_ingredients):
		if ConvertUnitServer == 1:
			Amount = convert_containers(indx)
		else:
			Amount = ingredients[indx]["amount"]
			Unit = ingredients[indx]["unit"]
		if Scale != 1 or ConvertUnitServer == 1:
			new_recipe_data = new_recipe_data.replace("AMOUNT#", str(Amount * Scale) + " ")
			new_recipe_data = new_recipe_data.replace("UNIT#", TargetUnit + " ")
			new_recipe_data = new_recipe_data.replace("INGREDIENT#", str(ingredients[indx]["name"]) + " (orig: " + str(ingredients[indx]["originalString"]) + ")" + "\n<p>AMOUNT#UNIT#INGREDIENT#</p>")
		else:
			new_recipe_data = new_recipe_data.replace("AMOUNT#UNIT#INGREDIENT#", str(ingredients[indx]["originalString"]) + "\n<p>AMOUNT#UNIT#INGREDIENT#</p>")
	new_recipe_data = new_recipe_data.replace("<p>AMOUNT#UNIT#INGREDIENT#</p>", "")

	num_steps = len(steps)
	for indx in range(0, num_steps):
		new_recipe_data = new_recipe_data.replace("STEP#", str(steps[indx]["number"]) + ". " + str(steps[indx]["step"]) + "\n<p>STEP#</p>")
	new_recipe_data = new_recipe_data.replace("<p>STEP#</p>", "")



	f_new_html_recipe.write(new_recipe_data)
	f_new_html_recipe.close()
	f_new_html_recipe = file(ProjectPath + FilenameCurrentHTMLRecipe, 'w')
	f_new_html_recipe.write(new_recipe_data)


#######################################################################
#######################################################################

edit_html_template()
















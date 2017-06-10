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
from common_functions import *

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
	debug(Debug, "{" + ingredientName + ",\t" + sourceUnit + ",\t" + TargetUnit + "}")
	ConversionTableIndx = 0
	TargetUnitExist = False
	SourceUnitExist = False

	# checking if all necessary conversion data exist in DB
	for ConversionTableIndx in xrange(0, ConversionTableSize):
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
		debug(Debug, ConvertContainersResponse.body)
		if ConversionTableIndx < ConversionTableSize - 1:
			debug(Debug, "ingredient exist")
			if TargetUnitExist == True:
				debug(Debug, "only source unit is missing")
				ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["sourceUnit"]] = ConvertContainersResponse.body["sourceAmount"]
			else:
				debug(Debug, "target unit is missing --> add entry to dictionary")
				ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["targetUnit"]] = ConvertContainersResponse.body["targetAmount"]
				if SourceUnitExist == False:
					debug(Debug, "source unit is missing --> add entry to dictionary")
					ConversionTable[ConversionTableIndx][ConvertContainersResponse.body["sourceUnit"]] = ConvertContainersResponse.body["sourceAmount"]
			debug(Debug, ConversionTable[ConversionTableIndx])
		else:
			debug(Debug, "create new dictionary for ingredient --> add both source and target")
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


def edit_html_template() :

	# files & paths:
	f_html_template = file(ProjectPath + FilenameHTMLtemplate, 'r')
	
	new_recipe_data = f_html_template.read()
	new_recipe_data = new_recipe_data.replace("recipeName", str(attributes[1]["title"]))
	new_recipe_data = new_recipe_data.replace("sourceURL", str(attributes[0]["sourceUrl"]))

	num_ingredients = len(ingredients)
	info("adding ingredients to recipe")
	debug(Debug, "num_ingredients: " + str(num_ingredients))
	debug(Debug, "ConvertUnitServer: " + str(ConvertUnitServer))
	debug(Debug, "scale: " + str(Scale))
	for indx in range(0, num_ingredients):
		debug(Debug, "--")
		debug(Debug, str(ingredients[indx]["name"]))
		if ConvertUnitServer == 1:
			debug(Debug, "using server to convert")
			Amount = convert_containers(indx)
			Unit = TargetUnit
		else:
			debug(Debug, "not using server to convert")
			Amount = ingredients[indx]["amount"]
			Unit = ingredients[indx]["unit"]
		if (int(Scale) == 1) and (int(ConvertUnitServer) == 0):
			debug(Debug, "using original string")
			new_recipe_data = new_recipe_data.replace("AMOUNT#UNIT#INGREDIENT#", str(ingredients[indx]["originalString"]) + "\n<p>AMOUNT#UNIT#INGREDIENT#</p>")
		elif (int(Scale) != 1) or (int(ConvertUnitServer) == 1):
			debug(Debug, "scale = " + str(Scale) + " server = " + str(ConvertUnitServer))
			new_recipe_data = new_recipe_data.replace("AMOUNT#", str(Amount * int(Scale)) + " ")
			new_recipe_data = new_recipe_data.replace("UNIT#", Unit + " ")
			new_recipe_data = new_recipe_data.replace("INGREDIENT#", str(ingredients[indx]["name"]) + " (orig: " + str(ingredients[indx]["originalString"]) + ")" + "\n<p>AMOUNT#UNIT#INGREDIENT#</p>")
		else:
			error("unknown settings")
	new_recipe_data = new_recipe_data.replace("<p>AMOUNT#UNIT#INGREDIENT#</p>", "")

	num_steps = len(steps)
	info("adding steps to recipe")
	for indx in range(0, num_steps):
		new_recipe_data = new_recipe_data.replace("STEP#", str(steps[indx]["number"]) + ". " + str(steps[indx]["step"]) + "\n<p>STEP#</p>")
	new_recipe_data = new_recipe_data.replace("<p>STEP#</p>", "")


	new_html_recipe_filename = attributes[1]["title"] + "_" + str(attributes[1]["id"]) + ".htm"
	f_new_html_recipe = file(ProjectPath + HTMLdir + "\\" + new_html_recipe_filename, 'w')
	info("writing new recipe to page \'" + HTMLdir + "\\" + new_html_recipe_filename + "\'")
	f_new_html_recipe.write(new_recipe_data)
	f_new_html_recipe.close()
	f_new_html_recipe = file(ProjectPath + FilenameCurrentHTMLRecipe, 'w')
	info("writing new recipe to page \'" + FilenameCurrentHTMLRecipe + "\'")
	f_new_html_recipe.write(new_recipe_data)


#######################################################################
#######################################################################


Debug, UrlNum, RealURL, Scale, TargetUnit, ConvertUnitServer = parseArgs()
edit_html_template()
















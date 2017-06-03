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


def convert_containers(TargetUnit, indx) :		
	# convert containers
	global GlobalNumUsedServer
	
	ingredientName = ingredients[indx]["name"]
	sourceAmount = str(ingredients[indx]["amount"])
	sourceUnit = ingredients[indx]["unit"]
	print("using server(" + str(GlobalNumUsedServer) + "): " + WordConvert)
	GlobalNumUsedServer += 1
	convert_containers_response = unirest.get(SpoonacularServer + WordConvert + 
												"ingredientName=" + ingredientName + 
												"&sourceAmount=" + sourceAmount + 
												"&sourceUnit=" + sourceUnit + 
												"&targetUnit=" + TargetUnit,
	  headers={
		"X-Mashape-Key": MyMashapeKey,
		"Accept": "application/json"
	  }
	)
	
	return convert_containers_response.body
	# example response:
	# {"sourceAmount":2.0,
	# "sourceUnit":"teaspoons",
	# "targetAmount":4.0,
	# "targetUnit":"grams",
	# "answer":"2 teaspoons cornstarch translates to 4 grams.",
	# "type":"CONVERSION"}
	

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
	
	for indx in range(0, ConstNumIngredientsTemplate):
		idx = str(indx)
		if indx < num_ingredients:
			if ConvertUnitServer == 1:
				ConvertedIngredients = convert_containers(TargetUnit, indx)
				Amount = ConvertedIngredients["targetAmount"]
				Unit = ConvertedIngredients["targetUnit"]
			else:
				Amount = ingredients[indx]["amount"]
				Unit = ingredients[indx]["unit"]
			if Scale != 1 or ConvertUnitServer == 1:
				new_recipe_data = new_recipe_data.replace("AMOUNT#" + idx + "#", str(Amount * Scale) + " ")
				new_recipe_data = new_recipe_data.replace("UNIT#" + idx + "#", str(Unit) + " ")
				new_recipe_data = new_recipe_data.replace("INGREDIENT#" + idx + "#", str(ingredients[indx]["name"]) + " (orig: " + str(ingredients[indx]["originalString"]) + ")")
			else:	
				new_recipe_data = new_recipe_data.replace("AMOUNT#" + idx + "#UNIT#" + idx + "#INGREDIENT#" + idx + "#", str(ingredients[indx]["originalString"]))
		else:
			new_recipe_data = new_recipe_data.replace("AMOUNT#" + idx + "#", "")
			new_recipe_data = new_recipe_data.replace("UNIT#" + idx + "#", "")
			new_recipe_data = new_recipe_data.replace("INGREDIENT#" + idx + "#", "")

	num_steps = len(steps)
	for indx in range(0, ConstNumStepsTemplate):
		idx = str(indx)
		if indx < num_steps:
			new_recipe_data = new_recipe_data.replace("STEP#" + idx + "#", str(steps[indx]["number"]) + ". " + str(steps[indx]["step"]))
		else:
			new_recipe_data = new_recipe_data.replace("STEP#" + idx + "#", "")


			
	f_new_html_recipe.write(new_recipe_data)


#######################################################################
#######################################################################

edit_html_template()
















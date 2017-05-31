# for python 2.7


import os

from recipe_objects import *

# consts:
num_ingredients_template = 35
project_path = str(os.environ.get('zoocheff_path')) # need to set envirronment var "zoocheff_path"

def save_recipe_data() :
	recipe_name = attributes[1]["title"]
	recipe_name = recipe_name.replace(' ', '_')
	
	os.system("mkdir " + recipe_name)
	os.system("copy recipe_objects.py " + project_path + recipe_name + "\\" + recipe_name  + "_objects.py")

def edit_html_template() :

	global steps
	# files & paths:
	html_template_filename = "html_template\zoo_cheff_templateDraft.htm"
	new_html_recipe_filename = attributes[1]["title"] + "_" + str(attributes[1]["id"]) + ".htm"

	f_html_template = file(project_path + html_template_filename, 'r')
	f_new_html_recipe = file(project_path + new_html_recipe_filename, 'w')

	new_recipe_data = f_html_template.read()
	
	new_recipe_data = new_recipe_data.replace("recipeName", str(attributes[1]["title"]))
	new_recipe_data = new_recipe_data.replace("sourceURL", str(attributes[0]["sourceUrl"]))

	num_ingredients = len(ingredients)
	# for indx in range(0, num_ingredients_template):
		# if indx < num_ingredients:
			# new_recipe_data = new_recipe_data.replace("AMOUNT#" + str(indx) + "#", str(ingredients[indx]["amount"]))
			# new_recipe_data = new_recipe_data.replace("UNIT#" + str(indx) + "#", str(ingredients[indx]["unit"]))
			# new_recipe_data = new_recipe_data.replace("INGREDIENT#" + str(indx) + "#", str(ingredients[indx]["name"]))
		# else:
			# new_recipe_data = new_recipe_data.replace("AMOUNT#" + str(indx) + "#", "")
			# new_recipe_data = new_recipe_data.replace("UNIT#" + str(indx) + "#", "")
			# new_recipe_data = new_recipe_data.replace("INGREDIENT#" + str(indx) + "#", "")
			
	for indx in range(0, num_ingredients_template):
		if indx < num_ingredients:
			new_recipe_data = new_recipe_data.replace("ORIGINALSTRING#" + str(indx) + "#", str(ingredients[indx]["originalString"]))
		else:
			new_recipe_data = new_recipe_data.replace("ORIGINALSTRING#" + str(indx) + "#", "")

			
	# new_recipe_data = new_recipe_data.replace("Instruction#" + "1" + "#", str(instructions))

	num_steps = len(steps)
	for indx in range(0, num_ingredients_template):
		if indx < num_steps:
			new_recipe_data = new_recipe_data.replace("STEP#" + str(indx) + "#", str(steps[indx]["number"]) + ". " + str(steps[indx]["step"]))
		else:
			new_recipe_data = new_recipe_data.replace("STEP#" + str(indx) + "#", "")


			
	f_new_html_recipe.write(new_recipe_data)




	# add_ingredients = 0
	# for line in f_html_template:

		# if add_ingredients == 1:
			# for indx in range(0, num_ingredients):
				# f_html_template.write(ingredients[indx]["amount"] + "\n")
			# add_ingredients = 0
			# break
		# if IngredientListPatternBelow in line:
			# add_ingredients = 1


	# {"id":6008,
	# "aisle":"Canned and Jarred",
	# "image":"https://spoonacular.com/cdn/ingredients_100x100/bouillon-cube.jpg",
	# "name":"beef bouillon",
	# "amount":4.0,
	# "unit":"cubes",
	# "unitShort":"cubes",
	# "unitLong":"cubes",
	# "originalString":"4 cubes beef bouillon, crumbled",
	# "metaInformation":["crumbled"]},



	# print(attributes[0]["sourceUrl"])

	# num_ingredients = len(ingredients)
	# for indx in range(0, num_ingredients):
		# print(ingredients[indx]["originalString"])
		
	# print(instructions)


#######################################################################
#######################################################################

save_recipe_data()
edit_html_template()


















# for python 2.7

# Response object:
# Upon receiving a response, Unirest returns the result in the form of an Object.
# This object should always have the same keys for each language regarding to the response details.
#
# Response.code - HTTP Response Status Code (Example 200)
# Response.headers- HTTP Response Headers
# Response.body- Parsed response body where applicable, for example JSON responses are parsed to Objects / Associative Arrays.
# Response.raw_body- Un-parsed response body

import os
import unirest
import ast
import re

MyMashapeKey = "OLG4YvEhlBmshydgWrzvOa8wDLRZp11XcsSjsnS0RwSQYKrzeE"


def rip_recipe(project_path, use_server, real_url) :
	# files & paths:
	raw_extract_output_filename = "raw_extract_output.txt"
	raw_analyzedInstructions_output_filename = "raw_analyzedInstructions_output.txt"

	# spoonacular server related:
	spoonacular_server = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
	extract = "extract?forceExtraction="
	forceExtraction = "false" # have no idea what this is doing
	analyzedInstructions = "/analyzedInstructions?stepBreakdown="
	stepBreakdown = "true"
	url = real_url.replace(':' , '%3A') # ':' = '%3A'
	url = real_url.replace('/' , '%2F') # '/' = '%2F'
	url_var = '&url='


	# fields to keep:
	keep_fields = ["originalString",
				  # "instructions",
				  "text"]


	if use_server == 1:
		# Extract Recipe from Website using API:
		print("using server")
		extract_response = unirest.get(spoonacular_server + extract + forceExtraction + url_var + url,
		  headers={
			"X-Mashape-Key": MyMashapeKey
		  }
		)

		# find recipe ID:
		keep = re.search('}],"id":(.+?),"', extract_response.raw_body)
		recipe_id = keep.group(1)
		# Analyzed Recipe Instructions using API:
		analyzedInstructions_response = unirest.get(spoonacular_server + recipe_id + analyzedInstructions + stepBreakdown,
		  headers={
			"X-Mashape-Key": MyMashapeKey,
			"Accept": "application/json"
		  }
		)

		# write the raw output to file
		f_raw_extract_output = file(project_path + raw_extract_output_filename, 'w') # open file for write
		f_raw_extract_output.write(extract_response.raw_body) # write raw data to file
		attributes_data = instructions_data = ingredients_dict_data = extract_response.raw_body # direct the raw extract_response to a new object for reordering

		f_raw_analyzedInstructions_output = file(project_path + raw_analyzedInstructions_output_filename, 'w') # open file for write
		f_raw_analyzedInstructions_output.write(analyzedInstructions_response.raw_body) # write raw data to file
		analyzedInstructions_data = analyzedInstructions_response.raw_body # direct the raw analyzedInstructions_response (from file) to a new objecj

	else:
		print("not using server")
		f_raw_extract_output = file(project_path + raw_extract_output_filename, 'r') # open file for read - assuming file exist from previouse runs!!
		attributes_data = instructions_data = ingredients_dict_data = f_raw_extract_output.read() # direct the raw extract_response (from file) to a new objecj

		f_raw_analyzedInstructions_output = file(project_path + raw_analyzedInstructions_output_filename, 'r') # open file for read - assuming file exist from previouse runs!!
		analyzedInstructions_data = f_raw_analyzedInstructions_output.read() # direct the raw analyzedInstructions_response (from file) to a new objecj

	f_raw_extract_output.close() # close file
	f_raw_analyzedInstructions_output.close() # close file

	# ****************************************************************************************************************************************
	# **************create ingredient dictionary in src file recipe_objects.py ***************************************************************

	# prepare comments:
	head_comment = "# coding: utf-8\n\n# these ingredients are based on a recipe from:\n# " + real_url # push comment in the start of buffer
	ingredients_dict_comment = "\n\n# a list of all ingrediednts:\n" # push comment in the start of buffer
	instructions_comment = "\n\n# recipe instructions:\n"
	attributes_comment = "\n\n# recipe attributes:\n"

	# create attributes dictionary:
	keep = re.search('{"(.+?),"extendedIngredients"', attributes_data)
	attributes_1 = keep.group(1)
	keep = re.search('}],"id":(.+?),"text"', attributes_data)
	attributes_2 = keep.group(1)
	attributes_data = 'attributes = [\n{"' + attributes_1 + '},\n'
	attributes_data = attributes_data + '{"id":' + attributes_2 + '}\n]\n'
	attributes_data = attributes_data.replace("false", '"false"')
	attributes_data = attributes_data.replace("true", '"true"')


	# create ingredient dictionary:
	remove = re.search('{"(.+?)\[', ingredients_dict_data) # get substring between '<phrase>(.+?)<prase>'
	ingredients_dict_data = ingredients_dict_data.replace('{"' + remove.group(1) + '[', "ingredients = [")

	remove = re.search('}],(.+?)div>"}', ingredients_dict_data) # get substring between '<phrase>(.+?)<prase>'
	ingredients_dict_data = ingredients_dict_data.replace('}],' + remove.group(1) + 'div>"}', "}\n]\n")

	ingredients_dict_data = ingredients_dict_data.replace("{","\n{")

	# create instructions string:
	keep = re.search('"text":"(.+?)","instructions"', instructions_data)
	instructions_data = 'instructions = "' + keep.group(1) + '"\n'


	# print(instructions_data)
	analyzedInstructions_data = analyzedInstructions_data.replace('[{"name":"","steps":[', 'steps = [\n')
	analyzedInstructions_data = analyzedInstructions_data.replace('},{"number":', '},\n{"number":')
	analyzedInstructions_data = analyzedInstructions_data.replace('null', 'None')
	analyzedInstructions_data = analyzedInstructions_data.replace('}]}]', '}]')

	recipe_objects_filename = "recipe_objects.py"
		
	# creating new py source "ingredients_dict.py"
	f_recipe_objects = file(project_path + recipe_objects_filename, 'w') # open file for write
	f_recipe_objects.write(head_comment + # write ingredients_dict and instructions data to file
						attributes_comment + attributes_data +
						ingredients_dict_comment + ingredients_dict_data +
						instructions_comment + instructions_data +
						analyzedInstructions_data)

	f_recipe_objects.close()




















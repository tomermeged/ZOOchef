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
from common_functions import *

def rip_recipe() :

	info("parsing: " + param.RealURL)
	
	global GlobalNumUsedServer
	
	SpoonacularFriendlyURL = param.RealURL
	SpoonacularFriendlyURL = SpoonacularFriendlyURL.replace(':' , '%3A') # ':' = '%3A'
	SpoonacularFriendlyURL = SpoonacularFriendlyURL.replace('/' , '%2F') # '/' = '%2F'
	debug(param.Debug, SpoonacularFriendlyURL)
	

	# Extract Recipe from Website using API:
	info("using server(" + str(GlobalNumUsedServer) + "): " + WordExtract)
	GlobalNumUsedServer += 1
	debug(param.Debug, "unirest.get with: " + SpoonacularServer + WordExtract + "forceExtraction=" + SwitchForceExtraction + "&url=" + SpoonacularFriendlyURL)
	extract_response = unirest.get(SpoonacularServer + WordExtract +
									"forceExtraction=" + SwitchForceExtraction +
									"&url=" + SpoonacularFriendlyURL,
	  headers={
		"X-Mashape-Key": MyMashapeKey
	  }
	)
	# write the raw output to file
	f_raw_extract_output = file(ProjectPath + FilenameRawExtractOutput, 'w') # open file for write
	responseToFile = extract_response.raw_body
	responseToFile = responseToFile.replace(',"sourceUrl":','\n,"sourceUrl":')
	responseToFile = responseToFile.replace('},','},\n')
	responseToFile = responseToFile.replace('"extendedIngredients":[','"\nextendedIngredients":[\n')
	responseToFile = responseToFile.replace('],','],\n')
	f_raw_extract_output.write(responseToFile) # write raw data to file
	f_raw_extract_output.close() # close file
	
	
	# find recipe ID:
	recipe_id = extract_response.body["id"]
	
	# Analyzed Recipe Instructions using API:
	info("using server(" + str(GlobalNumUsedServer) + "): " + WordAnalyzedInstructions)
	GlobalNumUsedServer += 1
	
	analyzedInstructions_response = unirest.get(SpoonacularServer + str(recipe_id) + "/" + WordAnalyzedInstructions +
												"stepBreakdown=" + SwitchStepBreakdown,
	  headers={
		"X-Mashape-Key": MyMashapeKey,
		"Accept": "application/json"
	  }
	)
	# write the raw output to file
	f_raw_analyzedInstructions_output = file(ProjectPath + FilenameRawAnalyzedInstructionsOutput, 'w') # open file for write
	responseToFile = analyzedInstructions_response.raw_body
	responseToFile = responseToFile.replace('},','},\n')
	f_raw_analyzedInstructions_output.write(responseToFile) # write raw data to file
	f_raw_analyzedInstructions_output.close() # close file
	
	return extract_response, analyzedInstructions_response

def create_recipe_objects_file(extract_response, analyzedInstructions_response) :

	attributes_data = instructions_data = ingredients_dict_data = extract_response.raw_body.replace('null', 'None') # direct the raw extract_response to a new object for reordering
	analyzedInstructions_data = analyzedInstructions_response.raw_body.replace('null', 'None') # direct the raw analyzedInstructions_response (from file) to a new object
	
	# prepare comments:
	head_comment = "# coding: utf-8\n\n# these ingredients are based on a recipe from:\n# " + param.RealURL # push comment in the start of buffer
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
	if extract_response.body["extendedIngredients"] != None:
		remove = re.search('{"(.+?)\[', ingredients_dict_data) # get substring between '<phrase>(.+?)<prase>'
		debug(param.Debug, remove.group(1))
		ingredients_dict_data = ingredients_dict_data.replace('{"' + remove.group(1) + '[', "ingredients = [")

	remove = re.search('}],(.+?)}', ingredients_dict_data) # get substring between '<phrase>(.+?)<prase>'
	ingredients_dict_data = ingredients_dict_data.replace('}],' + remove.group(1) + '}', "}\n]\n")

	ingredients_dict_data = ingredients_dict_data.replace("{","\n{")

	# create instructions string:
	keep = extract_response.body["text"]
	keep = keep.replace("\n", "\n\\")
	if keep != None:
		instructions_data = 'instructions = "' + keep + '"\n'
		analyzedInstructions_data = analyzedInstructions_data.replace('[{"name":"","steps":[', 'steps = [\n')
		analyzedInstructions_data = analyzedInstructions_data.replace('},{"number":', '},\n{"number":')
		analyzedInstructions_data = analyzedInstructions_data.replace('}]}]', '}]')
	else:
		prompt("no instructions found on page, please enter manually...")
		Instructions_from_user = raw_input("")
		instructions_data = "instructions = \"" + Instructions_from_user + "\"" + "\n"
		analyzedInstructions_data = "steps = [\n{\"number\":1,\"step\":\"" + Instructions_from_user + "\"}]"

	# creating new py source "recipe_objects.py"
	f_recipe_objects = file(ProjectPath + FilenameRecipeObjects, 'w') # open file for write
	f_recipe_objects.write(head_comment + # write ingredients_dict and instructions data to file
						attributes_comment + attributes_data +
						ingredients_dict_comment + ingredients_dict_data +
						instructions_comment + instructions_data +
						analyzedInstructions_data)

	f_recipe_objects.close()



# Debug, UrlNum, RealURL, Scale, TargetUnit, ConvertUnitServer = parseArgs()
param = parseArgs()
extract_response, analyzedInstructions_response = rip_recipe()
create_recipe_objects_file(extract_response, analyzedInstructions_response)













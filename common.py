

import os
import unirest
import ast
import re
import os

# functions:
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def info(string):
	print("INFO: " + str(string))

def debug(string):
	if Debug == 1:
		print("DEBUG: " + str(string))

# words:
WordParsedRecipesDB = "ParsedRecipesDB"
WordNone = "None"
WordExtract = "extract?"
WordAnalyzedInstructions = "analyzedInstructions?"
WordConvert = "convert?"

# Switches:
SwitchForceExtraction = "false" # have no idea what this is doing
SwitchStepBreakdown = "true"

# filenames:
FilenameRecipeObjects = "recipe_objects.py"
FilenameIngredientsDB = "Ingredients_DB.py"
FilenameRawExtractOutput = "raw_extract_output.txt"
FilenameRawAnalyzedInstructionsOutput = "raw_analyzedInstructions_output.txt"
FilenameCurrentHTMLRecipe = "latest.htm"


# consts:
ConstNumIngredientsTemplate = 35
ConstNumStepsTemplate = 35

# Global vars:
GlobalNumUsedServer = 0


# defs:
ChromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ProjectPath = str(os.environ.get('zoocheff_path')) # need to set envirronment var "zoocheff_path"
MyMashapeKey = "OLG4YvEhlBmshydgWrzvOa8wDLRZp11XcsSjsnS0RwSQYKrzeE"
SpoonacularServer = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
RealURLlist = [	"http://allrecipes.com/recipe/25678/beef-stew-vi/",
					"http://www.bbcgoodfood.com/recipes/1993645/vegetarian-casserole",
					"http://allrecipes.com/recipe/7402/carrot-cake-iii/",
					"http://www.olivegarden.com/recipe/baked-stuffed-artichokes-with-foccacia/man-imp-reci-prd-18",
					"http://www.fitnessmagazine.com/recipe/chicken/mediterranean-chicken-and-pasta/",
					"http://www.foodnetwork.com/recipes/emeril-lagasse/homemade-buttermilk-recipe.html",
					"http://cooking.nytimes.com/recipes/1016605-the-only-ice-cream-recipe-youll-ever-need",
					"http://www.carine.co.il/page_298"]

# controls:
ForceUseServerExtract = 0
UrlNum = 4
RealURL = RealURLlist[UrlNum] # number 3 & 4 are not parsed correctly
Scale = 1
ConvertUnitServer = 1
TargetUnit = "grams"
Debug = 1


# common names:
FilenameRecipeObjectsUnique = RealURL
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('https://', '')
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('http://', '')
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('www.', '')
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('<', '.')	# < (less than)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('>', '.')	# > (greater than)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace(':', '.')	# : (colon)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('"', '.')	# " (double quote)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('/', '.')	# / (forward slash)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('\\', '.')	# \ (backslash)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('|', '.')	# | (vertical bar or pipe)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('?', '.')	# ? (question mark)
FilenameRecipeObjectsUnique = FilenameRecipeObjectsUnique.replace('*', '.')	# * (asterisk)
FilenameRecipeObjectsUnique = str(FilenameRecipeObjectsUnique + ".py")

SpoonacularFriendlyURL = RealURL
SpoonacularFriendlyURL = SpoonacularFriendlyURL.replace(':' , '%3A') # ':' = '%3A'
SpoonacularFriendlyURL = SpoonacularFriendlyURL.replace('/' , '%2F') # '/' = '%2F'

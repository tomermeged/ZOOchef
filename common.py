

import os
import unirest
import ast
import re
import os
import subprocess

# words:
WordNone = "None"
WordExtract = "extract?"
WordAnalyzedInstructions = "analyzedInstructions?"
WordConvert = "convert?"

# Switches:
SwitchForceExtraction = "false" # have no idea what this is doing
SwitchStepBreakdown = "true"

# directories:
HTMLdir = "html"
Debugdir = "debug"
ParsedRecipesDBdir = "ParsedRecipesDB"

# filenames:
FilenameRecipeObjects = "recipe_objects.py"
FilenameIngredientsDB = "Ingredients_DB.py"
FilenameRawExtractOutput = Debugdir + "\\raw_extract_output.txt"
FilenameRawAnalyzedInstructionsOutput = Debugdir + "\\raw_analyzedInstructions_output.txt"
FilenameCurrentHTMLRecipe = "latest.htm"
FilenameHTMLtemplate = HTMLdir + "\\zoo_cheff_templateDraft.htm"


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
					"http://www.olivegarden.com/recipe/baked-stuffed-artichokes-with-foccacia/man-imp-reci-prd-18", # not parsed correctly
					"http://www.fitnessmagazine.com/recipe/chicken/mediterranean-chicken-and-pasta/", # not parsed correctly
					"http://www.foodnetwork.com/recipes/emeril-lagasse/homemade-buttermilk-recipe.html",
					"http://cooking.nytimes.com/recipes/1016605-the-only-ice-cream-recipe-youll-ever-need",
					"http://www.carine.co.il/page_298"]




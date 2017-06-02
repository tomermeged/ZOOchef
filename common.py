

import os
import unirest
import ast
import re
import os

# consts:
ConstNumIngredientsTemplate = 35


# defs:
GlobalProjectPath = str(os.environ.get('zoocheff_path')) # need to set envirronment var "zoocheff_path"
GlobalMyMashapeKey = "OLG4YvEhlBmshydgWrzvOa8wDLRZp11XcsSjsnS0RwSQYKrzeE"
GlobalSpoonacularServer = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
RealURLlist = [	"http://allrecipes.com/recipe/25678/beef-stew-vi/",
					"http://www.bbcgoodfood.com/recipes/1993645/vegetarian-casserole",
					"http://allrecipes.com/recipe/7402/carrot-cake-iii/",
					"http://www.olivegarden.com/recipe/baked-stuffed-artichokes-with-foccacia/man-imp-reci-prd-18",
					"http://www.fitnessmagazine.com/recipe/chicken/mediterranean-chicken-and-pasta/",
					"http://www.foodnetwork.com/recipes/emeril-lagasse/homemade-buttermilk-recipe.html",
					"http://cooking.nytimes.com/recipes/1016605-the-only-ice-cream-recipe-youll-ever-need",
					"http://www.carine.co.il/page_298"]


# controls:
GlobalExtractResponseServer = 0 # no need to use server when developing code!!, use just to create the basic "raw_ouput" once
GlobalRealURL =	RealURLlist[0] # number 3 & 4 are not parsed correctly
GlobalScale = 1
GlobalConvertUnitServer = 0
TargetUnit = "grams"

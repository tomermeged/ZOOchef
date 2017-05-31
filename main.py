# for python 2.7

# cmd:
# e:
# E:\tomermeg\Dropbox\projects\ZOOchef\src
# python.exe main.py

import os
import rip_recipe
# import edit_html_template
project_path = str(os.environ.get('zoocheff_path')) # need to set envirronment var "zoocheff_path"
use_server = 0 # no need to use server when developing code!!, use just to create the basic "raw_ouput" once
real_url_list = [	"http://allrecipes.com/recipe/25678/beef-stew-vi/",
					"http://www.bbcgoodfood.com/recipes/1993645/vegetarian-casserole",
					"http://allrecipes.com/recipe/7402/carrot-cake-iii/",
					"http://www.olivegarden.com/recipe/baked-stuffed-artichokes-with-foccacia/man-imp-reci-prd-18",
					"http://www.fitnessmagazine.com/recipe/chicken/mediterranean-chicken-and-pasta/",
					"http://www.foodnetwork.com/recipes/emeril-lagasse/homemade-buttermilk-recipe.html",
					"http://cooking.nytimes.com/recipes/1016605-the-only-ice-cream-recipe-youll-ever-need",
					"http://www.carine.co.il/page_298"]

real_url =	real_url_list[0] # number 3 & 4 are not parsed correctly
print("parsing: " + real_url)

# os.system("findstr /m /S \"http://allrecipes.com/recipe/25678/beef-stew-vi/\" ./*") # checks if was already parsed
rip_recipe.rip_recipe(project_path, use_server, real_url)

# have to seperate programs - the recipe_object,py is ready only at the end of "rip_recipe"
os.system("python.exe edit_html_template.py")

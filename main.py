# for python 2.7

# to run do the following in cmd:
# e:
# E:\tomermeg\Dropbox\projects\ZOOchef\src
# python.exe main.py

from common import *

# checks if was already parsed:
FindObjectsFile = str(find(FilenameRecipeObjectsUnique, ProjectPath + WordParsedRecipesDB))
if FindObjectsFile == WordNone or ForceUseServerExtract == 1:
	os.system("python.exe rip_recipe.py") # have to seperate programs - the recipe_object.py is live
	os.system("mkdir " + ProjectPath + WordParsedRecipesDB)
	os.system("copy recipe_objects.py " + ProjectPath + WordParsedRecipesDB + "\\" + FilenameRecipeObjectsUnique)
else:
	info("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)
	os.system("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)


os.system("python.exe edit_html_template.py")








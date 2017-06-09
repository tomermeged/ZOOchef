# for python 2.7

# to run do the following in cmd:
# e:
# E:\tomermeg\Dropbox\projects\ZOOchef\src
# example: python.exe main.py --URL 0 -s 3 -c grams

from common import *
from common_functions import *

Debug, UrlNum, RealURL, Scale, TargetUnit, ConvertUnitServer = parseArgs()


# controls & parameters:
ForceUseServerExtract = 0
if int(UrlNum) != -1:
	RealURL = RealURLlist[int(UrlNum)]



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



# checks if was already parsed:
FindObjectsFile = str(find(FilenameRecipeObjectsUnique, ProjectPath + WordParsedRecipesDB))
if FindObjectsFile == WordNone or ForceUseServerExtract == 1:
	os.system("python.exe rip_recipe.py" + " --debug " + str(Debug) + " --URL " + RealURL) # have to seperate programs - the recipe_object.py is live
	os.system("mkdir " + ProjectPath + WordParsedRecipesDB)
	os.system("copy recipe_objects.py " + ProjectPath + WordParsedRecipesDB + "\\" + FilenameRecipeObjectsUnique)
else:
	info("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)
	os.system("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)


os.system("python.exe edit_html_template.py" + " --debug " + str(Debug) + " --scale " + str(Scale) + " --convert " + TargetUnit)








# for python 2.7

# to run do the following in cmd:
# e:
# E:\tomermeg\Dropbox\projects\ZOOchef\src
# example: python.exe main.py --URL 0 -s 3 -c grams

# subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)

from common import *
from common_functions import *
import platform


info("using python " + platform.python_version())



Debug, UrlNum, RealURL, Scale, TargetUnit, ConvertUnitServer = parseArgs()


# controls & parameters:
ForceUseServerExtract = 0
if int(UrlNum) != -1:
	RealURL = RealURLlist[int(UrlNum)]



FilenameRecipeObjectsUnique = url_to_filename(RealURL)
FilenameRecipeObjectsUnique = str(FilenameRecipeObjectsUnique + ".py")

run_cmd_devNull("if not exist " + ProjectPath + ParsedRecipesDBdir  + " mkdir " + ProjectPath + ParsedRecipesDBdir)
run_cmd_devNull("if not exist " + ProjectPath + HTMLdir  + " mkdir " + ProjectPath + HTMLdir)
run_cmd_devNull("if not exist " + ProjectPath + Debugdir  + " mkdir " + ProjectPath + Debugdir)

# checks if was already parsed:
FindObjectsFile = str(find(FilenameRecipeObjectsUnique, ProjectPath + ParsedRecipesDBdir))
if FindObjectsFile == WordNone or ForceUseServerExtract == 1:
	run_cmd("python.exe rip_recipe.py" + " --debug " + str(Debug) + " --URL " + RealURL)
	run_cmd_devNull("copy recipe_objects.py " + ProjectPath + ParsedRecipesDBdir + "\\" + FilenameRecipeObjectsUnique)
else:
	debug(Debug, "copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)
	run_cmd_devNull("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)

run_cmd("python.exe edit_html_template.py" + " --debug " + str(Debug) + " --scale " + str(Scale) + " --convert " + TargetUnit)






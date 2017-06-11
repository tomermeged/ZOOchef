#!/usr/bin/python

from common import *
from common_functions import *
import platform
import cgi, cgitb
import webbrowser


# info("using python " + platform.python_version())

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

param = arguments()

# Get data from fields

RealURL  = form.getvalue('URL')
if RealURL != None:
	param.RealURL  = RealURL
Scale  = form.getvalue('Scale')
if Scale != None:
	param.Scale  = Scale
TargetUnit  = form.getvalue('unit')
if TargetUnit != None:
	param.TargetUnit  = TargetUnit

# controls & parameters:
ForceUseServerExtract = 0
if int(param.UrlNum) != -1:
	param.RealURL = RealURLlist[int(param.UrlNum)]

FilenameRecipeObjectsUnique = url_to_filename(param.RealURL)
FilenameRecipeObjectsUnique = str(FilenameRecipeObjectsUnique + ".py")

run_cmd_devNull("if not exist " + ProjectPath + ParsedRecipesDBdir  + " mkdir " + ProjectPath + ParsedRecipesDBdir)
run_cmd_devNull("if not exist " + ProjectPath + HTMLdir  + " mkdir " + ProjectPath + HTMLdir)
run_cmd_devNull("if not exist " + ProjectPath + Debugdir  + " mkdir " + ProjectPath + Debugdir)

# checks if was already parsed:
FindObjectsFile = str(find(FilenameRecipeObjectsUnique, ProjectPath + ParsedRecipesDBdir))
if FindObjectsFile == WordNone or ForceUseServerExtract == 1:
	run_cmd("python.exe rip_recipe.py" + " --debug " + str(param.Debug) + " --URL " + param.RealURL)
	run_cmd_devNull("copy recipe_objects.py " + ProjectPath + ParsedRecipesDBdir + "\\" + FilenameRecipeObjectsUnique)
else:
	# debug(param.Debug, "copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)
	run_cmd_devNull("copy " + FindObjectsFile + " " + ProjectPath + FilenameRecipeObjects)

run_cmd("python.exe edit_html_template.py" + " --debug " + str(param.Debug) + " --scale " + str(param.Scale) + " --convert " + param.TargetUnit)

webbrowser.open('file://' + ProjectPath + FilenameCurrentHTMLRecipe)



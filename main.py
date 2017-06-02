# for python 2.7

# cmd:
# e:
# E:\tomermeg\Dropbox\projects\ZOOchef\src
# python.exe main.py

from common import *


# checks if was already parsed:
# os.system("findstr /m /S \"http://allrecipes.com/recipe/25678/beef-stew-vi/\" ./*") 

# have to seperate programs - the recipe_object.py is live
os.system("python.exe rip_recipe.py")

os.system("python.exe edit_html_template.py")








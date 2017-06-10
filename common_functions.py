

import getopt
import sys
import os
import subprocess

Debug = 0
UrlNum = -1
RealURL = ""
Scale = 1
TargetUnit = "NA"
ConvertUnitServer = 0

###############################################
##### find func ###############################
global find
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


###############################################
##### info (log) func #########################
global error
def error(string):
	print("ERROR: " + str(string))
	exit(1)
	
###############################################
##### info (log) func #########################
global info
def info(string):
	print("INFO: " + str(string))

	
###############################################
##### info (log) func #########################
global prompt
def prompt(string):
	print("PROMPT: " + str(string))


###############################################
##### debug (log) func ########################
global debug
def debug(Debug, string):
	if int(Debug) == 1:
		if len(string) > 100:
			print("****")
			print("DEBUG: " + str(string))
			print("****")
		else:
			print("DEBUG: " + str(string))


###############################################
##### run_cmd func ########################
global run_cmd
def run_cmd(cmd): 	
	retval = subprocess.call(cmd, shell=True)
	if  retval != 0:
		error(cmd + "\nreturned with error (" + str(retval) + ")")

		

###############################################
##### run_cmd func ########################
global run_cmd_devNull
def run_cmd_devNull(cmd):
	# dev/null file
	FNULL = open(os.devnull, 'w')
	retval = subprocess.call(cmd, stdout=FNULL, shell=True)
	FNULL.close()
	if  retval != 0:
		error(cmd + "returned with error (" + str(retval) + ")")

		

###############################################
##### url_to_filename func ########################
global url_to_filename
def url_to_filename(url):
	filename = url
	filename = filename.replace('https://', '')
	filename = filename.replace('http://', '')
	filename = filename.replace('www.', '')
	filename = filename.replace('<', '.')	# < (less than)
	filename = filename.replace('>', '.')	# > (greater than)
	filename = filename.replace(':', '.')	# : (colon)
	filename = filename.replace('"', '.')	# " (double quote)
	filename = filename.replace('/', '.')	# / (forward slash)
	filename = filename.replace('\\', '.')	# \ (backslash)
	filename = filename.replace('|', '.')	# | (vertical bar or pipe)
	filename = filename.replace('?', '.')	# ? (question mark)
	filename = filename.replace('*', '.')	# * (asterisk)
	return filename


###############################################
##### parseArgs func ##########################
def parseArgs():
	global Debug
	global UrlNum
	global RealURL
	global Scale
	global TargetUnit
	global ConvertUnitServer
	
	cmdLine = " ".join(sys.argv)
	info(cmdLine)
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'd:N:U:s:c:'
		, ['debug=', 'UrlNum=', 'URL=','scale=','convert='])

	except getopt.GetoptError:
		error("Incorrect arguments")
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-d', '--debug'):
			Debug = arg
		elif opt in ('-N', '--UrlNum'):
			UrlNum = arg		
		elif opt in ('-u', '--URL'):
			RealURL = arg
		elif opt in ('-s', '--scale'):
			Scale = arg
		elif opt in ('-c', '--convert'):
			TargetUnit = arg
			if arg != "NA":
				ConvertUnitServer = 1
			else:
				ConvertUnitServer = 0
				
	debug(Debug, "Debug: " + str(Debug))
	debug(Debug, "UrlNum: " + str(UrlNum))
	debug(Debug, "RealURL: " + RealURL)
	debug(Debug, "Scale: " + str(Scale))
	debug(Debug, "TargetUnit: " + TargetUnit)
	debug(Debug, "ConvertUnitServer: " + str(ConvertUnitServer))
	
	return Debug, UrlNum, RealURL, Scale, TargetUnit, ConvertUnitServer
	
	
	
	
	

################################################################################################
################################################################################################

















import getopt
import sys
import os

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
##### debug (log) func ########################
global debug
def debug(Debug, string):
	if int(Debug) == 1:
		print("DEBUG: " + str(string))


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















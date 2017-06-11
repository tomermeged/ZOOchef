

import getopt
import sys
import os
import subprocess

class arguments(object):
	# def __init__(Debug=0, UrlNum=-1, RealURL="", Scale=1, TargetUnit="NA", ConvertUnitServer=0):
		# self.Debug = Debug
		# self.UrlNum = UrlNum
		# self.RealURL = RealURL
		# self.Scale = Scale
		# self.TargetUnit = TargetUnit
		# self.ConvertUnitServer = ConvertUnitServer
	def __init__(self):
		self.Debug = 0
		self.UrlNum = -1
		self.RealURL = ""
		self.Scale = 1
		self.TargetUnit = "NA"
		self.ConvertUnitServer = 0
		
		

# Debug = 0
# UrlNum = -1
# RealURL = ""
# Scale = 1
# TargetUnit = "NA"
# ConvertUnitServer = 0

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
	cmdArgs = arguments()
	
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
			cmdArgs.Debug = arg
		elif opt in ('-N', '--UrlNum'):
			cmdArgs.UrlNum = arg
		elif opt in ('-u', '--URL'):
			cmdArgs.RealURL = arg
		elif opt in ('-s', '--scale'):
			cmdArgs.Scale = arg
		elif opt in ('-c', '--convert'):
			cmdArgs.TargetUnit = arg
			if arg != "NA":
				cmdArgs.ConvertUnitServer = 1
			else:
				cmdArgs.ConvertUnitServer = 0
				
	debug(cmdArgs.Debug, "Debug: " + str(cmdArgs.Debug))
	debug(cmdArgs.Debug, "UrlNum: " + str(cmdArgs.UrlNum))
	debug(cmdArgs.Debug, "RealURL: " + cmdArgs.RealURL)
	debug(cmdArgs.Debug, "Scale: " + str(cmdArgs.Scale))
	debug(cmdArgs.Debug, "TargetUnit: " + cmdArgs.TargetUnit)
	debug(cmdArgs.Debug, "ConvertUnitServer: " + str(cmdArgs.ConvertUnitServer))
	
	return cmdArgs

################################################################################################
################################################################################################















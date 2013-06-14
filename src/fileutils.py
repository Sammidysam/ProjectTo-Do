#!/usr/bin/python

import os
import io
import json
import sys

# gets all immediate subdirectories of certain directory
# immediate subdirectories means no subdirectories of subdirectories
def getSubdirs(dir):
	return [name for name in os.listdir(dir)
			if os.path.isdir(os.path.join(dir, name))]

# gets the home directory
# /home/$USER for Linux, \Users\$USER for Windows
# though $USER is not a variable for Windows
def getHome():
	return os.path.expanduser("~")

# gets the location that the program files will be stored
def getInstallLocation():
	return getHome() + os.sep + ".todo"

# writes pretty JSON with UTF-8 encoding
def writeJson(data, file):
	with io.open(file, 'w', encoding="utf-8") as f:
		f.write(unicode(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)))

# the default Project To-Do JSON configuration
# projecthub is where all the projects are
# blacklist is an array of folders you don't want included
defaultJson = {"projecthub": getHome() + os.sep + "Documents" + os.sep + "Workspace",
				"blacklist": [".metadata"],
				"sizeX": "460",
				"sizeY": "270"}

# parses some json text that is an argument
# identifier tells what item you want to retrieve
def parseJson(data, identifier):
	if isinstance(data, basestring):
		if os.path.isfile(data):
			file = io.open(data)
			string = file.read()
			file.close()
			return json.loads(string)[identifier]
		else:
			return json.loads(data)[identifier]
	else:
		return data[identifier]

# returns a string representation of a file's data
def getFile(name):
	if not os.path.isfile(name):
		sys.stderr.write("File " + name + " cannot be read!\n")
	else:
		file = io.open(name)
		string = file.read()
		file.close()
		return string

# returns a json loads of the file
def getJson(name):
	if not os.path.isfile(name):
		sys.stderr.write("File " + name + " cannot be read!\n")
	else:
		return json.loads(getFile(name))

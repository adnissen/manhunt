#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
import yaml

def loadConfig():
	global config 
	config = yaml.load(open('config.yaml'))
	global apikey
	apikey = config["apikey"]

def writeApiKey(key):
	stream = file('config.yaml', 'w')
	config["apikey"] = key
	yaml.dump(config, stream)

def search(searchTerm):
	request = requests.get('http://nzbs.org/api?t=search&q='+ searchTerm + '&apikey=' + apikey)
	root = ET.fromstring(request.content)
	channel = root[0]
	numElems = channel[8].attrib
	if (numElems["total"] == '0'):
		print("No results")
		return
	print(channel[9][0].text)

loadConfig()
if (sys.argv[1] == '--apikey'):
	writeApiKey(sys.argv[2])
elif (len(sys.argv) >= 2):
	search(sys.argv[1])
else:
	print("useage: manhunt \"searchterm\"")
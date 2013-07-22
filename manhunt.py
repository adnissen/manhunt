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
	global resUrls
	global resNames
	resUrls = []
	resNames = []

	request = requests.get('http://nzbs.org/api?t=search&q='+ searchTerm + '&apikey=' + apikey)
	root = ET.fromstring(request.content)
	channel = root[0]
	numElems = channel[8].attrib
	if (numElems["total"] == '0'):
		print("No results")
		return
	for i in range(5):
		resNames.append(channel[9 + i][0].text)
		resUrls.append(channel[9 + i][2].text)
	for k in range(len(resNames)):
		print("[" + str(k + 1) + "] " + resNames[k])
	getInput()
def getInput():
	print('Entry to download: ')
	entry = input()
	if (entry == "q"):
		return
	while (entry > 5 or entry < 1):
		print('Please make a valid selection, or q to quit: ')
		entry = input()
		if (entry == "q"):
			return
	print(resUrls[entry])

loadConfig()

if (len(sys.argv) >= 2):
	search(sys.argv[1])
else:
	print("useage: manhunt \"searchterm\"")
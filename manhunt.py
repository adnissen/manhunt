#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
import yaml

def loadConfig():
	global config 
	global apikey
	global sabHost
	global sabPort
	global sabapiKey
	config = yaml.load(open('config.yaml'))
	apikey = config["apikey"]
	sabHost = config["sabHost"]
	sabPort = config["sabPort"]
	sabapiKey = config["sabapiKey"]

def startConfig():
	entry = raw_input("Enter your sabnzbd+ host: ")
	config["sabHost"] = entry
	entry = raw_input("Enter your sabnzbd+ port: ")
	config["sabPort"] = entry
	entry = raw_input("Enter your sabnzbd+ apikey: ")
	config["sabapiKey"] = entry;

	stream = file('config.yaml', 'w')
	yaml.dump(config, stream)

def writeApiKey(key):
	stream = file('config.yaml', 'w')
	config["apikey"] = key
	yaml.dump(config, stream)

def search(searchTerm):
	global resUrls
	global resNames
	resUrls = []
	resNames = []

	request = requests.get('http://nzbs.org/api?lang=EN&t=search&q='+ searchTerm + '&apikey=' + apikey)
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
	entry = raw_input('Entry to download: ')
	if (entry == 'q'):
		return
	while (int(entry) > 5 or int(entry) < 1):
		entry = raw_input('Please make a valid selection, or q to quit: ')
		if (entry == 'q'):
			return
	addToSab(resUrls[int(entry)], resNames[int(entry)])

def addToSab(url, name):
	sabUrl = "http://" + str(sabHost) + ":" + str(sabPort) + "/api?mode=addurl&name=" + str(url) + "&nzbname=" + str(name) + "&apikey=" + str(sabapiKey)
	print(sabUrl)


loadConfig()
if (len(sys.argv) == 2 and sys.argv[1] == "--config"):
	startConfig()
elif (len(sys.argv) >= 2):
	search(" ".join(sys.argv[1:]))
else:
	print("useage: manhunt \"searchterm\"")
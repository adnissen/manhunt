#!/usr/bin/python

import sys
import requests
import xml.etree.ElementTree as ET
import yaml

def loadConfig():
	global config
	global sabHost
	global sabPort
	global sabapiKey
	config = yaml.load(open('config.yaml'))
	sabHost = config["sabHost"]
	sabPort = config["sabPort"]
	sabapiKey = config["sabapiKey"]

def sabConfig():
	entry = raw_input("Enter your sabnzbd+ host: ")
	config["sabHost"] = entry
	entry = raw_input("Enter your sabnzbd+ port: ")
	config["sabPort"] = entry
	entry = raw_input("Enter your sabnzbd+ apikey: ")
	config["sabapiKey"] = entry;

	stream = file('config.yaml', 'w')
	yaml.dump(config, stream)

def addIndex():
	indexers = yaml.load(open('indexers.yaml'))
	name = raw_input("Name of indexer (example: nzbs.org): ")
	url = raw_input("Url of indexer (example: http://nzbs.org/): ")
	apikey = raw_input("Api Key (example: 60fa49af916bc402916eeec6440757e7): ")
	indexers[name] = [url, apikey]

	stream = file('indexers.yaml', 'w')
	yaml.dump(indexers, stream)

def writeApiKey(key):
	stream = file('config.yaml', 'w')
	config["apikey"] = key
	yaml.dump(config, stream)

def search(searchTerm):
	global resUrls
	global resNames
	resUrls = []
	resNames = []
	global total
	total = 1

	indexers = yaml.load(open('indexers.yaml'))
	for indexer in indexers:
		request = requests.get(indexers[indexer][0] + 'api?lang=EN&t=search&q='+ searchTerm + '&apikey=' + indexers[indexer][1])
		root = ET.fromstring(request.content)
		channel = root[0]
		numElems = channel[8].attrib
		if (numElems["total"] == '0'):
			print("No results")
			return
		for i in range(5):
			resNames.append(channel[9 + i][0].text)
			resUrls.append(channel[9 + i][2].text)
			print("[" + str(total) + "] " + resNames[i])
			total += 1
	getInput()

def getInput():
	entry = raw_input('Entry to download: ')
	if (entry == 'q'):
		return
	while (int(entry) > total or int(entry) < 1):
		entry = raw_input('Please make a valid selection, or q to quit: ')
		if (entry == 'q'):
			return
	addToSab(resUrls[int(entry) - 1], resNames[int(entry) - 1])

def addToSab(url, name):
	sabUrl = "http://" + str(sabHost) + ":" + str(sabPort) + "/api?mode=addurl&name=" + str(url) + "&nzbname=" + str(name) + "&apikey=" + str(sabapiKey)
	print(sabUrl)


loadConfig()
if (len(sys.argv) == 2 and sys.argv[1] == "--config"):
	sabConfig()
elif (len(sys.argv) == 2 and sys.argv[1] == "--addIndex"):
	addIndex()
elif (len(sys.argv) >= 2):
	search(" ".join(sys.argv[1:]))
else:
	print("useage: manhunt \"searchterm\"")
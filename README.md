manhunt.py
=======
**version 0.1**

a command-line tool to search newznab sites, display results, and send to sabnzbd+

**Warning! This is version 0.1, which means if everything isn't perfectly right it probably will crash! I'm still actively developing this and everything will be much more fool-proof in the future. You've been warned!**

###Requirements
====
- python 2.7 +

- pyyaml

- requests

###Installation
====
Make sure all the requirements are installed.

git clone this repository:

	git clone https://github.com/adnissen/manhunt.git

Configure the connection to sabnzbd+ by running:

	python manhunt.py --config
	
Add at least one indexer to search by running:

	python manhunt.py --addIndex
	
Search!

	python manhunt.py linux
	
###More Words
====
If it crashes, check to make sure everything in config.yaml and indexers.yaml is correct. Graceful error-handling will be in the next version.

Right now, it displays the top 5 results from each indexer. This will configurable in the next version.

import json
import sys

''' This file loads data into torchtext format in the form
		sentence \t predicate \t subj \t obj
'''

def getTopics(devSet):
	TRAINFILE = "../data/tuples-train.json"
	if devSet:
		TRAINFILE = "../data/tuples-dev.json"
	print("Extracting...", "\n")
	with open(TRAINFILE, encoding = "utf8") as f:
		json_set = json.load(f)
		dataset = json_set['data']
		print(json_set['version'])
	return dataset

def pairs(devSet):
	pairList = []
	data = getTopics(devSet)
	for topic in data:
		for paragraph in topic['paragraphs']:
			for pair in paragraph['pairs']:
				pairList.append(pair)
	return pairList


data = pairs(devSet=(sys.argv[1] == "dev"))


with open("../data/ore-" + sys.argv[1] + ".tsv", "w") as outFile:
	for pair in data:
		for tup in pair['tuples']:
			tupley = tup.strip().split("\t")
			subj = tupley[0][1:]
			pred = tupley[1]
			obj = tupley[2][:-1]
			outFile.write(pair['sentence'].replace('\t', "")
			 + "\t" + pred + "\t" + subj + "\t" + obj + "\n")
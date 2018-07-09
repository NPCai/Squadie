import json
import sys

''' This file loads data into opennmt format in the form (two files)
		sentence subj obj 
		tuple
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


with open("../data/opennmt-src-" + sys.argv[1] + ".tsv", "w") as src:
	with open("../data/opennmt-tgt-" + sys.argv[1] + ".tsv", "w") as tgt:
		for pair in data:
			for tup in pair['tuples']:
				tupley = tup.strip().split("\t")
				subj = tupley[0][1:]
				pred = tupley[1]
				obj = tupley[2][:-1]
				src.write(pair['sentence'].replace('\n', "") + " " + subj + " " + obj + "\n")
				tgt.write(pred + "\n")
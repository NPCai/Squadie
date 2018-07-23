import spacy
import json
from collections import defaultdict
import sys

# Creates tuples-train or tuples-dev which prints sentence tuple pairs in conjuction with the contextual paragraph

JSON_FILE = "../data/qaTuples-train.json"
SENT_FILE = "../data/tuples-train.json"
VERSION = "2.0v1.1"
num_tuples = 0

if len(sys.argv) > 1 and sys.argv[1] == "dev":
	JSON_FILE = "../data/qaTuples-dev.json"
	SENT_FILE = "../data/tuples-dev.json"


nlp = spacy.load('en')

def get_sentence(doc, int_pos):
	''' Gets the sentence for a character position '''
	for sentence in list(doc.sents):
		for token in sentence:
			if token.idx >= int_pos:
				return sentence.text

with open(JSON_FILE, encoding = "utf8") as f:
	dataset_json = json.load(f)
	dataset = dataset_json['data']

with open(SENT_FILE, "w", encoding = "utf8") as outFile:
	squadieJson = {"version": VERSION, "data": []}
	for topic in dataset:
		print(topic['title'])
		squadieTopic = {"title": topic['title'], "paragraphs": []}
		for blob in topic['paragraphs']:
			squadieParagraph = {"pairs": [], "context": blob["context"]}
			para = nlp(blob['context'])
			sentenceToTuples = defaultdict(lambda: [])
			for span in blob['qas']:
				if span['answer_start'] == None:
					continue
				sentence = get_sentence(para, span['answer_start'])
				sentenceToTuples[sentence].append(span['tuple'])
				num_tuples += 1
			for sentence, tupleList in sentenceToTuples.items():
				squadiePairs = {"sentence": sentence, "tuples": tupleList}
				squadieParagraph['pairs'].append(squadiePairs)
			squadieTopic['paragraphs'].append(squadieParagraph)
		squadieJson['data'].append(squadieTopic)
	json.dump(squadieJson, outFile, indent = 4, ensure_ascii = False)

print(num_tuples)
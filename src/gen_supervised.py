import spacy
import json
from collections import defaultdict

JSON_FILE = "../data/qaTuples.json"
SENT_FILE = "../data/training_tuples.txt"
VERSION = "2.0v1.0"

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
			for sentence, tupleList in sentenceToTuples.items():
				squadiePairs = {"sentence": sentence, "tuples": tupleList}
				squadieParagraph['pairs'].append(squadiePairs)
			squadieTopic['paragraphs'].append(squadieParagraph)
		squadieJson['data'].append(squadieTopic)
	json.dump(squadieJson, outFile, indent = 4, ensure_ascii = False)


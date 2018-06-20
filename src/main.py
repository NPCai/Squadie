import json
import vis as v
import spacy

VERSION = "2.0v1.0"
TRAINFILE = "../squad2/train-v2.0.json"
JSON_FILE = "../data/qaTuples.json"

nlp = spacy.load('en')
failures = 0
successes = 0


with open(TRAINFILE, encoding = "utf8") as f:
	dataset_json = json.load(f)
	dataset = dataset_json['data']

failList = []

with open(JSON_FILE, "w", encoding = "utf8"), as outFile:
	squadieJson = {"version": VERSION, "data": []}
	for topic in dataset: # Loads each topic into a dictionary
		squadieTopic = {"title": topic['title'], "paragraphs": []}
		for blob in topic['paragraphs']:
			squadieParagraph = {"qas": [], "context": blob["context"]}
			for span in blob['qas']: # Each qa has a question, id, and answers
				squadieQa = {"question": None, "id": span['id'], "answer": None, "tuple": None, "answer_start": None}
				if not span['is_impossible'] and len(span['question']) < 60: # Cut off at 60 characters because parser doesn't do well on long sentences
					q = span['question'].replace("\t", "")
					if q.endswith("."):
						q = q[:-1]
					if not q.endswith("?"):
						q += "?"
					shortAnswer = None
					shortAnswerStart = None
					for answerBlob in span['answers']:
						ans = answerBlob['text']
						if shortAnswer == None or len(ans) < len(shortAnswer):
							shortAnswer = ans
							shortAnswerStart = answerBlob['answer_start']
							successes = successes + 1
					sentence = list(nlp(q).sents)[0]
					x = v.parse(sentence, shortAnswer.replace("\t", ""))
					if x == None:
						failures = failures + 1
						failList.append(str(sentence) + " " + str(shortAnswer))
					else:
						successes = successes + 1
						print(x)
						squadieQa['question'] = q
						squadieQa['tuple'] = str(x)
						squadieQa['answer'] = shortAnswer
						squadieQa['answer_start'] = shortAnswerStart
				squadieParagraph['qas'].append(squadieQa)
			squadieTopic["paragraphs"].append(squadieParagraph)
		squadieJson["data"].append(squadieTopic)
	json.dump(squadieJson, outFile, indent = 4, ensure_ascii = False)
						
				
print("\n")
print("Number of failures: ", failures)
print("Number of successes: ", successes, "\n")

input("Press enter to see failures...\n")

for qa in failList:
	print(qa)
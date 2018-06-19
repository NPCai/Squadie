import json
import vis as v
import spacy

VERSION = "2.0v1.0"

nlp = spacy.load('en')
failures = 0
successes = 0


with open("../squad2/dev-v2.0.json", encoding = "utf8") as f:
	dataset_json = json.load(f)
	dataset = dataset_json['data']

failList = []

with open("../data/tuples.json", "w") as outFile:
	squadieJson = {"version": VERSION, "data": []}
	for topic in dataset: # Loads each topic into a dictionary
		squadieTopic = {"title": topic['title'], "paragraphs": []}
		for blob in topic['paragraphs']:
			squadieParagraph = {"qas": [], "context": blob["context"]}
			for span in blob['qas']: # Each qa has a question, id, and answers
				squadieQa = {"question": None, "id": span['id'], "answer": None, "tuple": None}
				if not span['is_impossible'] and len(span['question']) < 60:
					q = span['question'].replace("\t", "")
					if q.endswith("."):
						q = q[:-1]
					if not q.endswith("?"):
						q += "?"
					shortAnswer = None
					for answerBlob in span['answers']:
						ans = answerBlob['text']
						if shortAnswer == None or len(ans) < len(shortAnswer):
							shortAnswer = ans
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
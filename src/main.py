import json
import vis as v
import spacy

nlp = spacy.load('en')
failures = 0
successes = 0
with open("../squad2/dev-v2.0.json", encoding = "utf8") as f:
	dataset_json = json.load(f)
	dataset = dataset_json['data']

failList = []

for topic in dataset:
	print(topic['title'])
	for blob in topic['paragraphs']:
		for span in blob['qas']:
			if not span['is_impossible'] and len(span['question']) < 60:
				print(span['question'])
				shortAnswer = None
				failures = failures + 1
				for answerBlob in span['answers']:
					ans = answerBlob['text']
					if shortAnswer == None or len(ans) < len(shortAnswer):
						shortAnswer = ans
						successes = successes + 1
				sentence = list(nlp(span['question']).sents)[0]
				x = v.parse(sentence, shortAnswer)
				if x == None:
					failures = failures + 1
					failList.append(str(sentence) + " " + str(shortAnswer))
				else:
					successes = successes + 1
					print(x)
print("Number of failures: ", failures, "\n")
print("Number of successes: ", successes, "\n")

input("Press enter to see failures...\n")

for qa in failList:
	print(qa)
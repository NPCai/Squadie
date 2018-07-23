''' This file convers the News QA dataset from Maluuba '''
import csv
import vis
import spacy
from collections import Counter
import re
nlp = spacy.load('en')

def get_sentence(doc, int_pos):
	''' Gets the sentence for a character position '''
	for sentence in list(doc.sents):
		for token in sentence:
			if token.idx >= int_pos:
				return sentence.text
first = True

src_file = open("../data/news_qa_src.txt", "w")
tgt_file = open("../data/news_qa_tgt.txt", "w")

with open('../data/news_qa.csv', 'r', encoding = "utf8") as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	count = 0
	for row in spamreader:
		if first:
			first = False
			continue
		if len(row[1]) < 7: # or not vis.isWh(row[1]):
			continue
		doc = nlp(row[6])
		uniques = Counter()
		for str_tup in row[2].replace(",", "|").split("|"):
			arr = str_tup.split(":")
			if len(arr) == 2:
				tup = tuple(map(int, arr))
				uniques[tup] += 1
		if len(uniques) > 0:
			for r in uniques:
				if uniques[r] >= 2:
					sent_txt = get_sentence(doc, r[0])
					if sent_txt != get_sentence(doc, r[1]): # no way to know which sentence is right
						continue
					#print("Sentence: ", sent_txt.strip())
					#print("Question: ", row[1].strip())
					#print("Answer: ", row[6][r[0]:r[1]].strip())
					#print(row[5] != "")
					# We've found spacy does better parses on individual sentecnes so I'll create another doc object
					question = list(nlp(row[1].strip()).sents)[0]
					tupie = vis.parse(question, row[6][r[0]:r[1]].strip())
					if len(str(tupie)) > 5 and len(sent_txt) > 5:
						#print("Tuple: ", tupie)
						#print("------------------------------------\n\n\n\n\n")
						print(count)
						src_file.write(re.sub('\s+', ' ', sent_txt).strip() + "\r\n")
						tgt_file.write(re.sub('\s+', ' ', str(tupie)).strip() + "\r\n")
						
						count += 1
src_file.close()
tgt_file.close()
print(count)
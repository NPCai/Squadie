import spacy
from spacy import displacy

nlp = spacy.load('en')
docInput = input("Enter a sentence:  ")
doc = nlp(docInput)
for token in doc:
	print(str(token) + " " + token.dep_)
displacy.serve(doc, style='dep')
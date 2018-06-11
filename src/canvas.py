import spacy
from spacy import displacy

nlp = spacy.load('en')
docInput = input("Enter a sentence:  ")
doc = nlp(docInput)
displacy.serve(doc, style='dep')
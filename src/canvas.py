import spacy
from spacy import displacy

nlp = spacy.load('en')
doc = nlp(u'What does Thomas Edison think?')
displacy.serve(doc, style='dep')
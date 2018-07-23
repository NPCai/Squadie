import requests

URL = "http://localhost:8080/relationExtraction/text"


def triple(span):
	payload = {
	 "text": span,
	 "doCoreference": "true", 
	 "isolateSentences": "false", 
	 "format": "DEFAULT"
	 }

	r = requests.post(URL, data=payload)
	return t.text
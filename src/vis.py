import spacy

####################################################
################# HELPER MODULES ###################
####################################################

def descendants(sentence, ancestor, ignoreFirst, *includes): 
	''' Returns descendants of a node in-order '''
	sent = sentence
	if ancestor == None:
		return None, None
	descendants = ""
	descendantList = []
	if ignoreFirst and isWh(sent[0]):
		sent = sentence[1:]
	for token in sent:
		if ancestor.is_ancestor(token) or ancestor == token or token in includes:
			descendants += str(token) + " "
			descendantList.append(token)
	if (len(descendants) > 0):
		return descendants.strip(), descendantList
	else:
		return None, None

def isWh(token):
	return token.lower_ in ['who', 'what', 'where', 'when', 'why', 'how']


class Extract(object):

	def __init__(self, arg1=None, rel=None, arg2=None):
		self.arg1 = arg1
		self.rel = rel
		self.arg2 = arg2
	def __str__(self):
		return "<" + str(self.arg1) + "," + str(self.rel) + "," + str(self.arg2) + ">"

####################################################
################# PARSE ALGORITHMS #################
####################################################

def parse(sentence, answer):
	''' Test different parsing algorithms '''
	i = whoParse(sentence, answer)
	if i != None:
		return i
	i = genericParse(sentence, answer)
	if i != None:
		return i
	i = invertedParse(sentence, answer)
	if i != None:
		return i

def genericParse(sentence, answer):
	''' Generic catch-most parse algorithm for generating tuples '''
	arg1 = None
	arg2 = None
	prepChild = None
	pobjChild = None
	attrChilds = []
	for child in sentence.root.children:
		# Get the subject
		if child.dep_ == "nsubj":
			arg1 = descendants(sentence, child, True)[0]
		# Get the object
		elif child.dep_ == "prep":
			prepChild = child
		elif child.dep_.endswith("obj"):
			pobjChild = child
		elif child.dep_ == "attr":
			attrChilds.append(child)

	if arg1 == None:
		for attrToken in attrChilds:
			subject = True
			for child in attrToken.children:
				if child.dep_ == "prep" or child.dep_ == "advmod" or child.dep_ == "amod":
					subject = False
			if subject == True:
				arg1, _ = descendants(sentence, attrToken, False)

	if pobjChild != None: # There was no preposition
		arg2 = descendants(sentence, pobjChild, True, sentence.root)[0] # TODO: add in optional arguments

	elif prepChild != None: # There might be something under the prepChild
		arg2 = descendants(sentence, prepChild, True, sentence.root)[0]

	else: # No object
		for attrToken in attrChilds:
			obj = False
			print(attrToken)
			for child in attrToken.children:
				if child.dep_ == "prep" or child.dep_ == "advmod" or child.dep_ == "amod":
					obj = True
			if obj == True:
				arg2, _ = descendants(sentence, attrToken, False)
	print("Potential extract", Extract(arg1=arg1, arg2=arg2, rel=answer))
	if arg1 != None and arg2 != None:
		return Extract(arg1=arg1, arg2=arg2, rel=answer)
	return None

def invertedParse(sentence, answer):
	''' Used for when the attr points back to the what i.e. "what be" questions '''
	# The answer is the arg1
	# The poss or pobj group is the arg2
	# The nsubj group (minus poss/pobj group) is the relation
	if sentence[0].dep_ != "attr":
		return None
	arg2 = ""
	rel = []
	obj = []
	for child in sentence.root.children:
		if child.dep_ == "attr" or child.dep_ == "nsubj" and not isWh(child):
			_, rel = descendants(sentence, child, True) # Create superset
	for child in rel:
		if child.dep_ == "poss" or child.dep_.endswith("obj"):
			arg2, obj = descendants(sentence, child, True)
	rel = [token for token in rel if not token in obj]
	return Extract(arg1=answer, arg2=arg2, rel=''.join(str(i) + " " for i in rel).strip())


def whoParse(sentence, answer):
	''' Parser for "who be" questions '''
	arg1 = ""
	arg2 = ""
	rel = ""
	if sentence[0].dep_ != "nsubj":
		return None
	else:
		arg1 = answer

	print(sentence.root)
	pass
	# return Extract(arg1 = answer, arg2 = peepee, rel = ''.join(str(i) + " " for i in rel).strip())
	





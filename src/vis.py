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
	i = whoParseNsubj(sentence, answer)
	if i != None:
		return i
	i = whoParseAttr(sentence, answer)
	if i != None:
		return i
	i = genericParse(sentence, answer)
	if i != None:
		return i
	i = invertedParse(sentence, answer)
	if i != None:
		return i
	i = noObjParse(sentence, answer)
	return i

def genericParse(sentence, answer):
	''' Generic catch-most parse algorithm for generating tuples '''
	arg1 = None
	arg2 = None
	prepChild = None
	pobjChild = None
	attrChilds = []
	if sentence[0].dep_ == "attr":
		return None
	for child in sentence.root.children:
		if child.dep_ == "ccomp":
			arg2 = descendants(sentence, child, True, sentence.root)[0]
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

	if prepChild != None: # There was no preposition
		arg2 = descendants(sentence, prepChild, True, sentence.root)[0] # TODO: add in optional arguments

	elif pobjChild != None: # There might be something under the prepChild
		arg2 = descendants(sentence, pobjChild, True, sentence.root)[0]

	else: # No object
		for attrToken in attrChilds:
			obj = False
			for child in attrToken.children:
				if child.dep_ == "prep" or child.dep_ == "advmod" or child.dep_ == "amod":
					obj = True
			if obj == True:
				arg2, _ = descendants(sentence, attrToken, False)
	if arg1 != None and arg2 != None:
		print("Generic parse")
		return Extract(arg1=arg1, arg2=answer, rel=arg2)
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
	print("Inverted parse")
	return Extract(arg1=answer, arg2=arg2, rel=''.join(str(i) + " " for i in rel).strip())

def noObjParse(sentence, answer):
	''' Used when there is no object in the sentence '''
	print("Starting noobj parse")
	subjGroups = []
	for token in sentence:
		if token.dep_.endswith("obj"): 
			return None 
		if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
			subjGroups.append(descendants(sentence, token, True)[1])
	if len(subjGroups) == 0:
		return None
	trueSubjPos = len(subjGroups) - 1 # default to the last subj group
	if len(subjGroups) > 1: # have to find the true subject
		count = 0
		for group in subjGroups:
			for word in group:
				if word.pos_ == "PROPN":
					trueSubj = count
			count = count + 1
	arg1 = ''.join(str(i) + " " for i in subjGroups[trueSubjPos]).strip()
	rel = [i for i in sentence if not i in subjGroups[trueSubjPos]]
	return Extract(arg1=arg1, rel=''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in rel).strip(), arg2=answer)


def whoParseNsubj(sentence, answer):
		''' Parser for "who be" questions '''
		arg1 = ""
		arg2 = ""
		rel = []
		relBad = []

		if sentence[0].dep_ != "nsubj": # Checking to make sure this is the right algorithm to use
			return None
		else:
			arg1 = answer # arg1 just replace the who with the answer

		_, rel = descendants(sentence, sentence.root, True) # Gets the relation plus the relBad (lots of children!)

		for child in rel:
			if child.dep_ == "pobj":
				arg2, relBad = descendants(sentence, child, True) # Gets just the relBad children
				break

		rel = [token for token in rel if not token in relBad] # Finds the difference between the 2 lists
		return Extract(arg1 = answer, arg2 = arg2, rel = ''.join(str(i) + " " for i in rel).replace("?","").strip()) # Extracts all the juicy info

def whoParseAttr(sentence, answer):
	''' parse for who questions where the who is an attribute and not an Nsubj'''
	arg1 = []
	arg2 = []
	rel = []
	relBad = []
	pobj = True


	if sentence[0].dep_ != "attr" or sentence[0].lower_ != "who": # Checking to make sure the who is an attribute of the root
		return None
	else:
		for child in sentence:
			if child.dep_ == "pobj":
				pobj = True
				break
			else:
				pobj = False
				if child.dep_ == "nsubj" or child.dep_ == "attr" and not isWh(child):
					_, arg1 = descendants(sentence, child, True)
		
		if pobj == False:
			rel = sentence.root
			arg2 = answer
			return Extract(arg1 = ''.join(str(i) + " " for i in arg1).strip(), arg2 = arg2, rel = rel)


		if pobj == True:
			for child in sentence:
				if child.dep_ == "nsubj" or child.dep_ == "attr" and not isWh(child):
					_, relBad = descendants(sentence, child, True, sentence.root)
			
				if child.dep_ == "pobj":
					_, arg2 = descendants(sentence, child, True)
					arg1 = answer
			rel = [token for token in relBad if not token in arg2]
			return Extract(arg1 = arg1, arg2 = ''.join(str(i) + " " for i in arg2).strip(), rel = ''.join(str(i) + " " for i in rel).strip())
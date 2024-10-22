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
	return token.lower_ in ['who', 'what', 'where', 'when', 'why', 'how']#,'What','Where','When','Why','How']

def extractHelper(arg1, rel, arg2):
	if "list" in str(type(arg1)):
		arg1 = ''.join(str(i) + " " for i in arg1).replace("?","").strip()
	if "list" in str(type(rel)):
		rel = ''.join(str(i).replace("?","").strip() + " " for i in rel).replace("  "," ").strip()
	if "list" in str(type(arg2)):
		arg2 = ''.join(str(i) + " " for i in arg2).replace("?","").strip()
	return arg1, rel, arg2

class Extract(object):

	def __init__(self, arg1=None, rel=None, arg2=None):
		self.arg1 = arg1
		self.rel = rel
		self.arg2 = arg2
	def __str__(self):
		return "<" + str(self.arg1) + "\t" + str(self.rel) + "\t" + str(self.arg2) + ">"

def badExtract(i):
	if i == None or i.arg1 == None or str(i.arg1) == "" or i.rel == None or str(i.rel) == "" or i.arg2 == None or str(i.arg2) == "":
		return True
	return False

####################################################
################# PARSE ALGORITHMS #################
####################################################

def parse(sentence, answer):
	''' Test different parsing algorithms '''
	''' Each algorithm has a check that determines
	if it should be used '''
	i = whichParse(sentence, answer)
	if badExtract(i):
		i = threeOrFourParser(sentence, answer, False)
	if badExtract(i):
		i = whoParseNsubj(sentence, answer)
	if badExtract(i):
		i = whoParseAttr(sentence, answer)
	if badExtract(i):
		i = whereParse(sentence, answer)
	if badExtract(i):
		i = howParse(sentence, answer)
	if badExtract(i):
		i = genericParse(sentence, answer)
	if badExtract(i):
		i = invertedParse(sentence, answer)
	if badExtract(i):
		i = finalWhatParse(sentence, answer)
	if badExtract(i):
		i = noObjParse(sentence, answer)
	if badExtract(i):
		i = noSubjParse(sentence, answer)
	if badExtract(i):
		i =  threeOrFourParser(sentence, answer, True)
	if badExtract(i):
		return None
	print(sentence)
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
		if child.dep_ == "ccomp" or child.dep_ == "acomp":
			arg2 = descendants(sentence, child, True, sentence.root)[0]
		# Get the subject
		if child.dep_ == "nsubj":
			_,arg1 = descendants(sentence, child, True)
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
				_, arg1 = descendants(sentence, attrToken, False)
	
	if prepChild != None and pobjChild != None:
		arg2 = descendants(sentence, pobjChild, False, sentence.root)[0] + " " + descendants(sentence, prepChild, False)[0]
	elif prepChild != None: # There was no preposition
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
				arg2 = descendants(sentence, attrToken, False)[0]
	if arg1 != None and arg2 != None:
		print("Generic parse")
		stopwords = ['who', 'what', 'where', 'when', 'why', 'how']
		arg1 = [word for word in arg1 if word.lower_ not in stopwords]
		for words in stopwords:
			arg2.replace('words','')
			arg2.replace('  ', '')
		return Extract(arg1=''.join(str(i) + " " for i in arg1).strip(), arg2=answer, rel=arg2)
	return None

def finalWhatParse(sentence, answer):
	preps = ["as", "for", "in", "of", "by"]
	bes = ["was", "is", "be"]
	if not sentence[len(sentence) - 2].lower_ in preps: # Has to be - 2 because the question mark counts as part of the array so you have to account for that
		#print("Returnin none 1")
		return None
	if not sentence[1].lower_ in bes:
		#print("Returnin none 2")
		return None
	verbPos = None
	count = 0
	for token in sentence[:-2]:
		if token.pos_ == "VERB":
			verbPos = count
		count = count + 1
	if verbPos == None or verbPos == len(sentence) - 2:
		#print("Returnin none 3")
		return None
	arg1 = sentence[2:verbPos]
	rel = sentence[verbPos:len(sentence) - 1]
	x =  Extract(arg1=''.join(str(i) + " " for i in arg1).strip(), rel=''.join(str(i) + " " for i in rel).strip(), arg2=answer)
	print("Final what parse")
	return x

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
		if child.dep_ == "attr" or child.dep_ == "nsubj" or child.dep_ == "ccomp" and not isWh(child):
			_, rel = descendants(sentence, child, True) # Create superset
	if rel == None:
		return None
	for child in rel:
		if child.dep_ == "poss" or child.dep_.endswith("obj") or child.dep_ == "acomp":
			arg2, obj = descendants(sentence, child, True)
	rel = [token for token in rel if not token in obj]
	print("Inverted parse")
	return Extract(arg1 = answer, rel=''.join(str(i) + " " for i in rel).strip(), arg2 = arg2)


def invertedParseAcomp(sentence, answer):
	# Inverted parse algorithm when the child is an adjectival complement
	# Now obsolete
	arg1 = []
	arg2 = ""
	rel = []
	acomp = True
	for child in sentence:
		if child.dep_ == "acomp":
			acomp = True
			break
		else:
			acomp = False

	if acomp == False:
		return None
	else:
		for child in sentence:
			if child.dep_ == "nsubj" or child.dep_ == "pobj" and not isWh(child):
				_, arg1 = descendants(sentence, child, True)
		for child in sentence:
			if child.dep_ == "acomp":
				_, rel = descendants(sentence, child, True)
		arg2 = answer
	return Extract(arg1 = ''.join(str(i) + " " for i in arg1).strip(), arg2 = arg2, rel = ''.join(str(i) + " " for i in rel).strip())

def noObjParse(sentence, answer):
	''' Used when there is no object in the sentence '''
	subjGroups = []
	for token in sentence:
		if token.dep_.endswith("obj"): 
			return None 
		if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
			subjGroups.append(descendants(sentence, token, False)[1])
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
	for wh in rel:
		if isWh(wh) == True:
			rel.remove(wh)

	print("noObj parse")
	return Extract(arg1=arg1, rel=''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in rel).strip(), arg2=answer)

def noSubjParse(sentence, answer):
	'''Used when there is no subject in the sentence '''
	arg1 = []
	rel = []
	arg2 = []
	objCounter = 0
	nonObj = False
	noMoreObj = False
	for subjSearch in sentence:
		if "subj" in subjSearch.dep_ and not isWh(subjSearch):
			return None
	'''ideal strings used to model'''
	if "subj" in sentence[0].dep_: #The only subject is the who/what/when at the beginning of the sentence
		arg1 = answer
		for child in sentence:
			if "obj" in child.dep_ and objCounter == 0 or "advcl" in child.dep_ and objCounter == 0 or "xcomp" in child.dep_ and objCounter == 0:
				_, rel = descendants(sentence, child, True, sentence.root)
				objCounter += 1
				nonObj = True
			if "prep" in child.dep_:
				_, arg2 = descendants(sentence, child, True)
				for obj in arg2:
					print([i.dep_ for i in list(obj.rights)])
					if ('obj' in str([i.dep_ for i in list(obj.rights)]) and objCounter > 0) or ('obj' in str([i.dep_ for i in list(obj.rights)]) and nonObj == True):
						_, arg2 = descendants(sentence, child, True)
						noMoreObj = True
			if "obj" in child.dep_ and noMoreObj == False:
				_, arg2 = descendants(sentence,child,True)
		rel = [token for token in rel if not token in arg2]


	arg1, rel, arg2 = extractHelper(arg1, rel, arg2)
	print("No Subject Parse")
	return Extract(arg1 = arg1, rel = rel, arg2 = arg2)
def whichParse(sentence, answer):
	''' Parser for questions that start with which '''
	if sentence[0].lower_ != "which" or sentence[1].dep_ == "nsubj":
		return None
	subjGroup = None
	_, relGroup = descendants(sentence, sentence.root, True)
	if relGroup == None:
		return None
	objGroup = None
	objStr = None
	for token in sentence:
		if token.dep_ == "nsubj" and subjGroup == None:
			print("nsubj")
			_, subjGroup = descendants(sentence, token, True)
		if token.dep_.endswith("obj"):
			objStr, objGroup = descendants(sentence, token, True)
	if objGroup == None or subjGroup == None:
		return None
	relGroup = [i for i in relGroup if ((not i in subjGroup) and (not i in objGroup))]
	relGroup = [token for token in relGroup if token != sentence[0]]
	print("Which parse")
	return Extract(arg1=answer, rel=''.join(str(i).replace("?", "").replace(",", "").strip() + " " for i in relGroup).strip(), arg2=objStr)

def howParse(sentence, answer):
	''' Parser for questions that begin with the adverbial modifier how'''
	arg1 = []
	arg2 = []
	rel = []
	argument = False
	relTrue = False
	Object = False
	poss = False
	objTrue = False

	if sentence[0].lower_ != "how":
		return None
	if sentence[1].lower_ == "much" or sentence[1].lower_ == "many":
		arg1 = answer
		argument = False
		for child in sentence:
			if "subj" in child.dep_:
				_, arg2 = descendants(sentence, child, True)
			if "obj" in child.dep_:
				Object = True
		_, rel = descendants(sentence, sentence.root, True)
		rel = [token for token in rel if not token in arg2]
		stopwords = ['much','many']
		arg2 = [word for word in arg2 if word.lower_ not in stopwords]
		rel = [token for token in rel if token.lower_ not in stopwords]
		rel = [child for child in rel if "aux" not in child.dep_ or child.lower_ == "to"]

		if len(arg2) != 0:
			if sentence[1].lower_ == "much" and arg2[0].dep_ != "prep":
				arg2.insert(0, "in")

			if sentence[1].lower_ == "many" and Object == False:
				rel.insert(0, "number")
	
	elif sentence[1].lower_ == "did" or sentence[1].lower_ == "is":
		
		for child in sentence:
			if "obj" in child.dep_:
				_, rel = descendants(sentence, child, True, sentence.root)
			if "subj" in child.dep_:
				_, arg1 = descendants(sentence, child, True)

		arg2.append(answer)
		nlp = spacy.load('en')
		answerDep = nlp(answer)
		if sentence[1].lower_ != "is":
			for token in answerDep:
				if token.dep_ == "poss":
					arg2.insert(0,"with")
					poss = True
			if poss == False:
				arg2.insert(0,"by")
		else:
			arg2.insert(0,"as")
		argument = True
	
	elif "comp" in sentence[1].dep_ or sentence[1].dep_ == "advmod":
		for child in sentence:
			if "obj" in child.dep_:
				objTrue = True
		
		if objTrue == True and sentence[1].dep_ == "advmod":
			for children in sentence:
				if "obj" in children.dep_:
					_, arg1 = descendants(sentence, children, True)
			rel = sentence.root.lower_
			arg2.append(answer)
			for advmod in sentence:
				if advmod.dep_ == "advmod":
					arg2.append(advmod.lower_)	
		
		if objTrue == True and "comp" in sentence[1].dep_:
			for token in sentence:
				if "subj" in token.dep_:
					_, arg1 = descendants(sentence, token, True)
					break
			rel = sentence.root.lower_
			arg2.append(answer)
			for comp in sentence:
				if "comp" in comp.dep_:
					arg2.append(comp.lower_)

	else:
		return None

	print("How parse")
	arg1, rel, arg2 = extractHelper(arg1, rel, arg2)
	return Extract(arg1 = arg1, rel = rel, arg2 = arg2)

def whereParse(sentence, answer):
	''' Parser for questions that have where in them '''
	arg1 = []
	arg2 = []
	rel = []
	prep = False
	where = False
	other = False
	num = 0
	for token in sentence:
		if token.lower_ == "where":
			where = True
			break
	if where == False:
		return None
	else:
		if sentence.root.pos_ == "VERB":
			_, rootChildren = descendants(sentence, sentence.root, True) # Gets the relation plus the relBad (lots of children!)
			for token in rootChildren:
				if "comp" in token.dep_:
					rel.extend([sentence.root,token])
					other = True
			if other == False:
				rel.append(sentence.root)

			for tokenChild in rootChildren:
				if token.dep_ == "prep":
					rel.append(token)
					prep = True
				else:
					break
			arg2.append(answer)
			for child in rootChildren:
				if "nsubj" in child.dep_:
					_, arg1_temp = descendants(sentence, child, True)
					arg1_temp = ''.join(str(i) + " " for i in arg1_temp).strip()
					arg1.append(arg1_temp)
				if "obj" in child.dep_:
					_, arg1_temp2 = descendants(sentence, child, True)
					arg1_temp2 = ''.join(str(i) + " " for i in arg1_temp2).strip()
					arg1.extend([" in ",arg1_temp2])
	for token in rel:
		if token.pos_ == "VERB":
			num += 1

	rel = list(map(str,rel))
	rel = " ".join(rel).split()
	arg1 = ''.join(arg1).split()

	rel = [token for token in rel if not token in arg1]
	
	if prep == False:
		rel.append("in")
	
	if num == 2:
		rel.insert(1,"to")
		rel.insert(2,"be")
	
	print("Where parse")
	return Extract(arg1 = ''.join(str(i) + " " for i in arg1).strip(), rel = ''.join(str(i) + " " for i in rel).strip(), arg2 = ''.join(str(i).replace(",","").replace("?","") + " " for i in arg2).strip())

def whoParseNsubj(sentence, answer):
		''' Parser for "who be" questions '''
		arg1 = ""
		arg2 = ""
		rel = []
		relBad = []
		pobj = True
		dobj = True
		if sentence[0].dep_ != "nsubj" or sentence[0].lower_ != "who": # Checking to make sure this is the right algorithm to use
			return None
		else:
			arg1 = answer # arg1 just replace the who with the answer

		_, rel = descendants(sentence, sentence.root, True) # Gets the relation plus the relBad (lots of children!)

		for child in rel:
			if child.dep_ == "pobj":
				arg2, relBad = descendants(sentence, child, True) # Gets just the relBad children
				pobj = True
				break
			else:
				pobj = False
			
		if pobj == False:
			for child in rel:
				if child.dep_ == "dobj":
					arg2, relBad = descendants(sentence, child, True)
					dobj = True
					break
				else:
					dobj = False

		if dobj == False:
			for child in rel:
				if child.dep_ == "nsubj":
					arg2, relBad = descendants(sentence, child, True)
					break

		rel = [token for token in rel if not token in relBad] # Finds the difference between the 2 lists
		print("Who parse nsubj")
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
			print("Who parse attribute")
			return Extract(arg1 = arg1, arg2 = ''.join(str(i) + " " for i in arg2).strip(), rel = ''.join(str(i) + " " for i in rel).strip())

def threeOrFourParser(sentence, answer, force):
	''' Used if the question has 3 or 4 words or a catch all if every other parser has failed'''
	arg1 = []
	arg2 = []
	rel = []
	arg1Force = []
	if len(sentence.text.split()) >= 5 and force == False:
		return None
	else:
		if force == False:
			_, arg2 = descendants(sentence, sentence.root, True)
			arg2 = [token for token in arg2 if token != sentence.root]
			stopwords = ['percentage']
			arg2 = [word for word in arg2 if word.lower_ not in stopwords]
			arg1Force = arg2
			for child in sentence:
				print("Dependency is ",child.dep_,"\n")

				if child.pos_ == "VERB" and force == False:
					rel = child
					arg1 = answer

		if force == True:
			_, arg1 = descendants(sentence, sentence.root, True)
			arg1 = [tokeny for tokeny in arg1 if tokeny != sentence.root]
			stopwordsy = ['percentage']
			arg1 = [wordy for wordy in arg1 if wordy.lower_ not in stopwordsy]
			for coin in sentence:
				if coin.dep_ == "ROOT":
					rel.append(coin.lower_)
					arg2 = answer
				if force == True and coin.dep_ == "aux" and coin.lower_ == "did":
					print("reno")
					rel.insert(0,coin.lower_)
			arg1 = [token for token in arg1 if token.lower_ not in rel]

	arg1,rel,arg2 = extractHelper(arg1,rel,arg2)
	print("Three or four parser")
	return Extract(arg1 = arg1, rel = rel, arg2 = arg2)
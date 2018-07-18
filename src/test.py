import unittest
import vis as v
import spacy

class TestParseMethods(unittest.TestCase):


	'''TODO
	What party is favored in Bedigo and Geelong? Labor
	### What percentage of Victorians are Christian? 61%        (Just get rid of percentage in answer)
	### What city is the capital of Victoria? Melbourne         (Just get rid of what)
	### When was Victoria first settled? 1803                   (Just get rid of when)
	### How much Victorian farmland is farmed in grains? 26,000 square kilometres        (Get rid of much (whatever dependency that may be))        <26,000 square kilometres,farmed,much Victorian farmland is in grains>
	### How many tonnes of tomatoes does Victoria produce? 270,000
	### How many Victorians are non-religious? 20% 				(Number in the relation (basically replace how many with number))     <Victorians,number non-religious,20%>
	### How many seats does Victoria have in the Senate? 12
	### How many Catholic schools were in Victoria? 489
	### How many full time teachers does Victoria have? 63,519
	### How much of Australia's milk is produced in Victoria? two-thirds

	
	### How much imported oil came from the Middle East? 71%
	### How much capital did Danish law require to start a company? 200,000 Danish krone
	### How much dust is blown out of the Sahara each year? 182 million tons



	How high are Victoria's alpine regions? 2,000 m
	How are Victorian cabinet members chosen? elected
	How did the Huguenots defend themselves? their own militia
	How did the revocation restrict Huguenot travel? prohibited emigration
	For how long did Huguenots continue to use French names? 10 years
	How is dioxygen most simply described? covalent double bond
	How is the O2 molecule referred to in its ground state? O
	How long ago did oxygen reach 10% of its present level? 1.7 billion years ago
	How was scarcity managed in many countries? rationing
	How often does the European Council meet? each six months
	How are the explanations supported?
	How large can ctenophora grow? 1.5m
	How do ctenophores control buoyancy? It is uncertain
	How are the combs spaced? evenly
	How are eggs and sperm released? pores in the epidermis
	How old were the fossils found in China? 515 million years
	How far is Fresno from Los Angeles? 220 miles
	How far apart are some of the neighborhood's features? few hundred feet
	How would one describe the summers in Fresno? hot and dry (Dont mess with this)
	How old are the gravestones that reference the plague? 1338-39


	<the neighbourhood's features 



	
	### <Dioxygen, most simply described, as covalent double bond>
	### <The O2 molecule, refferred to in its ground state, as O>
	
	###	<two-thirds,produced in victoria, of australia's milk
	### <270,000, tonnes of tomatoes produce, victoria>
	### <20%,number are non - religious,Victorians>
	### <26,000 square kilometres,is farmed in grains,in Victorian farmland>

	

	'''
	def setUp(self):
		nlp = spacy.load('en')
		self.doc = nlp(u'''In what year did Tesla go to Budapest?
			 What was Konstantin Mereschkowski's career?
			 What are chloroplasts descended from?
			 How do chloroplasts trigger the plant's immune system?
			 What does ATP synthase change into ATP?
			 How many G3P molecules leave the cycle?
			 What is an alternate way to make starch?
			 When might Starch grains become overly large?
			 What is the primary purpose of chloroplasts?
			 Who was Alfred S Brown?
			 Who won the Nobel Prize in 1905?''')
		self.ans = ["1899", "biologist", "Cyanobacteria", "by purposely damaging their photosynthetic system",
			"phosphorylate adenosine diphosphate", "3000", "glucose monomers",
			"high atmospheric CO2 concentrations", "to conduct photosynthesis", "a Western Union superintendent",
			"Phillip Leonard"]
		self.test = nlp(u'''How many miles south of Edinburgh is Newcastle?
			 How many miles from the north Sea is Newcastle?
			 What network is Newcastle a member of?
			 What county was Newcastle a part of until 1400?
			 What is the regional nickname for Newcastle and its surrounding area?
			 Who directed Luther away from self-reflection and towards the merits of Christ?
			 Who is the primary rival of the Harvard Crimson hockey team?''')
		self.anstest = ["103 miles", "8.5 mi", "Eurocities", "Northumberland", "Geordie", "Johann von Staupitz", "Cornell"]

		self.martinLuther = nlp(u'''Where did Martin Luther go to school?
			 How did Luther describe the University of Erfurt?
			 How early did Luther say he had to awaken every day?
			 How did Luther describe his learning at the university?
			 In what year did Luther get his degree?''')
		self.martinLuterTest = ["University of Erfurt", "beerhouse and whorehouse", "at four", "rote learning", "1505"]

		self.longer = nlp(u'''What party is favored in Bedigo and Geelong?
			What bongo is bongo in bongo?''')
		self.longerTest = ["Labor","bongo"]

		self.oneSentence = nlp(u"how many copies of 4 sold in the first week?")
		self.oneSentenceTest = ["310,000"]

	'''def test_descendants(self):
		sentences = list(self.doc.sents)
		for sentence, answer in zip(sentences, self.ans):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n")
		self.assertTrue(True)

	def test_england(self):
		sentences = list(self.test.sents)
		for sentence, answer in zip(sentences, self.anstest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n")
		self.assertTrue(True)

	def test_luther(self):
		sentences = list(self.martinLuther.sents)
		for sentence, answer in zip(sentences, self.martinLuterTest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n")
		self.assertTrue(True)

	def test_longerTest(self):
		sentences = list(self.longer.sents)
		for sentence, answer in zip(sentences, self.longerTest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n\n")
		self.assertTrue(True)'''

	def test_oneSentence(self):
		sentences = list(self.oneSentence.sents)
		for sentence, answer in zip(sentences, self.oneSentenceTest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n\n")
		self.assertTrue(True)


if __name__ == '__main__':
	unittest.main()
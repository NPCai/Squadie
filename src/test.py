import unittest
import vis as v
import spacy

class TestParseMethods(unittest.TestCase):


	'''TODO
	What party is favored in Bedigo and Geelong? Labor
	What percentage of Victorians are Christian? 61%        (Just get rid of percentage in answer)
	How many Victorians are non-religious? 20%  <Victorians,number non-religious,20%         (Number in the relation (basically replace how many with number))
	What city is the capital of Victoria? Melbourne         (Just get rid of what)


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

		self.oneSentence = nlp(u"Where is the Asian influence strongest in Victoria?")
		self.oneSentenceTest = ["Bendigo"]

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
		self.assertTrue(True)'''

	def test_longerTest(self):
		sentences = list(self.longer.sents)
		for sentence, answer in zip(sentences, self.longerTest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n\n")
		self.assertTrue(True)

	def test_oneSentence(self):
		sentences = list(self.oneSentence.sents)
		for sentence, answer in zip(sentences, self.oneSentenceTest):
			print(sentence, answer)
			print(v.parse(sentence, answer), "\n\n")
		self.assertTrue(True)


if __name__ == '__main__':
	unittest.main()
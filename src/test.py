import unittest
import vis as v
import spacy

class TestParseMethods(unittest.TestCase):


	'''TODO'''
	



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

		self.superBowl = nlp(u'''Which NFL team represented the AFC at Super Bowl 50?
			 Where did Super Bowl 50 take place?
			 Which NFL team won Super Bowl 50?
			 What color was used to emphasize the 50th anniversary of the Super Bowl?
			 What was the theme of Super Bowl 50?
			 What day was the game played on?
			 What is the AFC short for?
			 What does AFC stand for?
			 If Roman numerals were used, what would Super Bowl 50 have been called?
			 Which Carolina Panthers player was named Most Valuable Player?
			 How many appearances have the Denver Broncos made in the Super Bowl?
			 What year was the Carolina Panthers franchise founded?
			 What team did the Panthers defeat?
			 Who did the Broncos prevent from going to the Super Bowl?
			 Who did the Panthers beat in the NFC Championship Game?
			 ''')
		self.superBowlTest = ["Denver Broncos", "Levi's Stadium", "Denver Broncos", "Gold", "Golden anniversary", 
			 "February 7th, 2016", "American Football Conference", "American Football Conference", "Super Bowl L", "Cam Newton", "Eight", "1995"
			 "Arizona Cardinals", "New England Patriots", "Arizona Cardinals"]

		self.oneSentence = nlp(u"Where are Jersey and Guernsey?")
		self.oneSentenceTest = ["Channel Islands"]

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

	def test_superBowl(self):
		sentences = list(self.superBowl.sents)
		for sentence, answer in zip(sentences, self.superBowlTest):
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
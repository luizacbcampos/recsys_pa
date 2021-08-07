import numpy as np


#---------------- The Setup Class ----------------------

class setup(object):
	''' 
		Setup arguments class
	'''
	
	def __init__(self, k, epochs, l_rt, reg, random, verbose, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball', accents=True):
		self.k = k
		self.epochs = epochs
		self.learning_rate = l_rt
		self.regularizer = reg
		self.random = random
		self.verbose = verbose
		self.tokenization = self.set_tokenization(lower_, number, apostrophe, punctuation, stem, accents)

	def set_tokenization(self, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball', accents=True):
		self.tokenization = {
			'lower_':lower_,
			'number':number, 
			'apostrophe':apostrophe,
			'punctuation':punctuation,
			'stem':stem,
			'accents':accents
			}
	def get_tokenization(self):
		lower_ = self.tokenization['lower_']
		number = self.tokenization['number']
		apostrophe = self.tokenization['apostrophe']
		punctuation = self.tokenization['punctuation']
		stem = self.tokenization['stem']
		accents = self.tokenization['accents']
		
		return lower_, number, apostrophe, punctuation, stem, accents

	def __init__(self, k, epochs, l_rt, reg, random, verbose):
		self.k = k
		self.epochs = epochs
		self.learning_rate = l_rt
		self.regularizer = reg
		self.random = random
		self.verbose = verbose
	def get(self):
		return self.k, self.epochs, self.learning_rate, self.regularizer, self.random, self.verbose
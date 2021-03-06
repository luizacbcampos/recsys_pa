import numpy as np


#---------------- The Setup Class ----------------------

class Setup(object):
	''' 
		Setup arguments class
	'''
	
	def __init__(self, verbose, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball', 
		accents=True, drop_list=None, weights=np.array([3/40, 11/40, 10/40, 6/40, 7/40, 3/40]), perc=True):
		self.verbose = verbose
		self.tokenization = self.set_tokenization(lower_, number, apostrophe, punctuation, stem, accents)
		self.drop_list = drop_list
		self.weights = weights
		self.perc = perc

	def set_tokenization(self, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball', accents=True):
		tok = {
			'lower_':lower_,
			'number':number, 
			'apostrophe':apostrophe,
			'punctuation':punctuation,
			'stem':stem,
			'accents':accents
			}
		return tok

	def get_drop_list(self):
		return self.drop_list
	
	def get_weights(self):
		return self.weights
	
	def get_perc(self):
		return self.perc
	
	def get_tokenization(self):
		lower_ = self.tokenization['lower_']
		number = self.tokenization['number']
		apostrophe = self.tokenization['apostrophe']
		punctuation = self.tokenization['punctuation']
		stem = self.tokenization['stem']
		accents = self.tokenization['accents']

		return lower_, number, apostrophe, punctuation, stem, accents

	def get(self):
		return self.verbose, self.tokenization, self.drop_list, self.weights, self.perc
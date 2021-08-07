import numpy as np


#---------------- The Setup Class ----------------------

class setup(object):
	''' 
		Setup arguments class
	'''
	
	def __init__(self, k, epochs, l_rt, reg, random, verbose):
		self.k = k
		self.epochs = epochs
		self.learning_rate = l_rt
		self.regularizer = reg
		self.random = random
		self.verbose = verbose
	
	def get_tokenization(self):
		return

	def __init__(self, k, epochs, l_rt, reg, random, verbose):
		self.k = k
		self.epochs = epochs
		self.learning_rate = l_rt
		self.regularizer = reg
		self.random = random
		self.verbose = verbose
	def get(self):
		return self.k, self.epochs, self.learning_rate, self.regularizer, self.random, self.verbose
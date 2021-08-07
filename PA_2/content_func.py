import numpy as np

#my imports
import tokenizer
from tokenizer import create_word_set


class Content(object):
	'''
		Content setting class
	'''
	def __init__(self, content_dict):
		self.content_dict = content_dict
		self.wordSet = create_word_set(content_dict)




# ---------- Similarity calculations -----



def cossine_similarity(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	#if its not
	cos_sim = (np.array(a) @ np.array(b).T) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim

def faster_for_short(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	cos_sim = np.inner(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim


# ---------- Category possibilities -----

def genre_list():
	'''
		Returns all possible genres
	'''
	lista = ['Film-Noir', 'Crime', 'Documentary', 'Sport', 'Horror', 'Sci-Fi', 'Western', 'Short', 'Fantasy',
	'Animation', 'Talk-Show', 'Comedy', 'Biography', 'Game-Show', 'Drama', 'News', 'History', 'Adult', 'War',
	'Action', 'Music', 'Musical', 'Adventure', 'Mystery', 'Reality-TV', 'Thriller', 'Family', 'Romance']
	return lista

def show_unique_from_list(content_dict, col):
	'''
		Show get_unique_from_list
	'''
	value_set = get_unique_from_list(content_dict, col)
	print("Unique values for {}".format(col))
	print(value_set)


def get_unique_from_list(content_dict, col):
	value_set = set()
	for dicio in content_dict:
		if type(dicio[col]) == list:
			for value in dicio[col]:
				value_set.add(value)
	return value_set


# ---------- One Hot Enconding -----------

def genre_one_hot(movie_genres):
	'''
		Generates a One-Hot enconding for the genres
	'''
	one_hot = {g:0 for g in genre_list()}
	
	if type(movie_genres) == list:
		for g in movie_genres:
			one_hot[g] = 1
	return one_hot


# ---------- Wrapper for tests -------

def pass_this(content_dict):
	#get_unique_from_list(content_dict, col='Genre')

	for dicio in content_dict:
		#print(genre_one_hot(dicio['Genre']))

		if type(dicio['Plot']) == str:
			a = tokenizer.tokenize(dicio['Plot'])
			#print(a)


if __name__ == '__main__':
	from functools import partial
	from timer import time_a_function, compare_many_functions

	a = 1
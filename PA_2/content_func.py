import numpy as np
import pandas as pd

#my imports
import tokenizer
from tokenizer import create_word_set_and_dict


class Content(object):
	'''
		Content setting class
	'''
	def __init__(self, content_dict):
		self.content_dict = content_dict
		#self.wordSet, self.token_dict = create_word_set_and_dict(content_dict)
		self.genre_ratings, self.genre_votes, self.total_ratings, self.total_votes = get_ratings_info(content_dict)
		self.avg_rating = self.set_avg_rating()
		self.genre_mean = self.set_genre_mean()

	def set_avg_rating(self):
		return self.total_ratings/self.total_votes
	
	def get_avg_rating(self):
		return self.avg_rating

	def set_genre_mean(self):
		genre_mean = {}
		for g,r in self.genre_ratings.items():
			genre_mean[g] = r/self.genre_votes[g]
		return genre_mean

	def get_movie_mean_genre_rating(self, genre_list):
		'''
			Genres have equal influence
		'''
		genres_mean = [m for g,m in self.genre_mean.items() if g in genre_list]
		mean = sum(genres_mean)/len(genre_list)
		return mean

	def get_movie_avg_genre_rating(self, genre_list):
		'''
			Genres avg by vote count
		'''
		ratings, votes = [],[]
		for g in genre_list:
			ratings.append(self.genre_ratings[g])
			votes.append(self.genre_votes[g])
		
		avg = sum(ratings)/sum(votes)
		return avg

# ---------- Similarity calculations -----


def cossine_similarity(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	#if its not
	cos_sim = (np.array(a) @ np.array(b).T) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim

def faster_for_short(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	cos_sim = np.inner(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim


# ---------- Ratings information -----

def make_short_dict(content_dict):

	short = []
	for dicio in content_dict:
		short.append({'Genre': dicio['Genre'], 'imdbVotes': dicio['imdbVotes'], 'imdbRating': dicio['imdbRating'] })
	
	return short

def get_ratings_info(content_dict):

	genre_ratings = dict.fromkeys(genre_list(), 0)
	genre_votes = dict.fromkeys(genre_list(), 0)
	total_ratings = 0
	total_votes = 0

	for dicio in content_dict:
		total_ratings += dicio['imdbRating'] * dicio['imdbVotes']
		total_votes += dicio['imdbVotes']
		for genre in dicio['Genre']:
			genre_ratings[genre]+= dicio['imdbRating'] * dicio['imdbVotes']
			genre_votes[genre]+= dicio['imdbVotes']
	
	return genre_ratings, genre_votes, total_ratings, total_votes

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

	c = Content(content_dict)
	genre_list = ['Action', 'Thriller']
	print(c.get_avg_rating())
	print("Mean: ", c.get_movie_mean_genre_rating(genre_list))
	print("Avg: ", c.get_movie_avg_genre_rating(genre_list))
	print(c.genre_mean)
	
	print("---")
	genre_ratings, genre_votes, total_ratings, total_votes = get_ratings_info(content_dict)
	print('total_ratings = {}, total_votes = {}'.format(total_ratings, total_votes))
	print('genre_ratings = {}, genre_votes = {}'.format(genre_ratings, genre_votes))

	for dicio in content_dict:
		#print(genre_one_hot(dicio['Genre']))

		if type(dicio['Plot']) == str:
			a = tokenizer.tokenize(dicio['Plot'])
			#print(a)


if __name__ == '__main__':
	from functools import partial
	from timer import time_a_function, compare_many_functions

	a = 1
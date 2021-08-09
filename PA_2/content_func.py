import numpy as np
import pandas as pd

#my imports
import tokenizer as tok


class Content(object):
	'''
		Content setting class
	'''
	def __init__(self, content_dict):
		self.content_dict = content_dict
		self.tfidf_dict, self.tfidf_dict_sqrd = tok.create_TFIDF(content_dict)
		self.genre_ratings, self.genre_votes, self.total_ratings, self.total_votes = get_ratings_info(content_dict)
		self.avg_rating = self.set_avg_rating()
		self.genre_mean = self.set_genre_mean()
		self.quantile = self.set_movie_quantile()
		self.content_dict = self.set_weighted_rating()
		self.one_hot_dict = self.set_one_hot_dict()
		self.avg_weight_rating, self.weight_genre_mean = self.set_avg_weight_ratings()


	def set_avg_rating(self):
		return self.total_ratings/self.total_votes
	
	def set_genre_mean(self):
		genre_mean = {}
		for g,r in self.genre_ratings.items():
			genre_mean[g] = r/self.genre_votes[g]
		return genre_mean

	def set_movie_quantile(self):
		votes = []
		for item_id, dicio in self.content_dict.items():
			votes.append(dicio['imdbVotes'])
		return np.quantile(votes, 0.1)

	def set_weighted_rating(self):
		C = self.avg_rating
		m = self.quantile
		
		def weighted_rate(v, R):
  			return (v/(v+m) * R)+(m/(v+m) * C)

		for item_id, dicio in self.content_dict.items():
			
			if self.content_dict[item_id]['imdbVotes'] == 0:
				self.content_dict[item_id]['weighted_rate'] = 0
			else:
				self.content_dict[item_id]['weighted_rate'] = weighted_rate(v=dicio['imdbVotes'], R=dicio['imdbRating'])
		return self.content_dict

	def set_avg_weight_ratings(self):
		genre_ratings, genre_votes, total_ratings, total_votes = get_ratings_info(self.content_dict, column='weighted_rate')
		avg_weight_rating = total_ratings/total_votes
		genre_mean = {}
		for g,r in genre_ratings.items():
			genre_mean[g] = r/genre_votes[g]
		return avg_weight_rating, genre_mean

	def set_one_hot_dict(self):
		
		one_hot_dicio = {}
		for item_id, dicio in self.content_dict.items():
			one_hot_dicio[item_id] = vectorize_one_hot(genre_one_hot(dicio['Genre'])) #alredy in vector shape
		return one_hot_dicio
	
	def get_content_dict(self):
		return self.content_dict

	def get_avg_rating(self):
		return self.avg_rating

	def get_movie_quantile(self):
		return self.quantile

	def get_avg_weight_rating(self):
		return self.avg_weight_rating

	def get_weight_genre_mean(self):
		return self.weight_genre_mean

	def get_item_tfidf_dict(self, item):
		return self.tfidf_dict[item]

	def get_item_tfidf_dict_sqrd(self, item):
		return self.tfidf_dict_sqrd[item]
	
	def get_content_dict_item(self, item, col):
		return self.content_dict[item][col]

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

	def get_one_hot_dict(self):
		return self.one_hot_dict

# ---------- Similarity calculations -----


def cossine_similarity(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	#if its not
	cos_sim = (np.array(a) @ np.array(b).T) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim

def cossine_call(a, b):
	if np.any(a) and np.any(b):
		return short_array_cos_sim(a,b)
	return 0
def short_array_cos_sim(a=[3, 45, 7, 2], b=[2, 54, 13, 15]):
	cos_sim = np.inner(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))
	return cos_sim

def cos_items(item1, item2, content):
	
	sim = 0

	item1_tfidf = content.get_item_tfidf_dict(item1)
	item2_tfidf = content.get_item_tfidf_dict(item2)
	for word in item1_tfidf.keys():
		if word in item2_tfidf:
			sim += item1_tfidf[word] * item2_tfidf[word]

	if sim == 0:
		return 0

	item1_tfidf_dict_sqrd = content.get_item_tfidf_dict_sqrd(item1)
	item2_tfidf_dict_sqrd = content.get_item_tfidf_dict_sqrd(item2)
	
	if  item1_tfidf_dict_sqrd == 0 or item2_tfidf_dict_sqrd == 0:
		return 0
	
	return (sim/(item1_tfidf_dict_sqrd * item2_tfidf_dict_sqrd))

# ---------- Ratings information -----

def make_short_dict(content_dict):

	short = []
	for dicio in content_dict:
		short.append({'Genre': dicio['Genre'], 'imdbVotes': dicio['imdbVotes'], 'imdbRating': dicio['imdbRating'] })
	
	return short

def get_ratings_info(content_dict, column='imdbRating'):

	genre_ratings = dict.fromkeys(genre_list(), 0)
	genre_votes = dict.fromkeys(genre_list(), 0)
	total_ratings = 0
	total_votes = 0

	for item_id, dicio in content_dict.items():
		total_ratings += dicio[column] * dicio['imdbVotes']
		total_votes += dicio['imdbVotes']
		for genre in dicio['Genre']:
			genre_ratings[genre]+= dicio[column] * dicio['imdbVotes']
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
	for item_id, dicio in content_dict.items():
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

def vectorize_one_hot(one_hot):
	return np.array(list(one_hot.values()))

def genres_avg_user(user_dict, one_hot_dict):
	ratings_sum = np.array([0]*len(genre_list()))
	genres_count = np.array([0]*len(genre_list()))

	for item_id, rating in user_dict.items():
		ratings_sum += rating*one_hot_dict[item_id]
		genres_count += one_hot_dict[item_id]

	genres_count[genres_count == 0] = 1 # replacing 0s with 1s
	avg_user_genre = ratings_sum/genres_count
	
	return avg_user_genre

def similarity_calculations(item, user_dict, content, start_perc=0.2):
	
	plot_rating, plot_sim, qtd_plot = 0, 0, len(content.get_content_dict_item(item, col='Plot')) 
	genre_rating, genre_sim, qtd_genre = 0, 0, len(content.get_content_dict_item(item, col='Genre'))

	if qtd_genre == 0 and qtd_plot == 0: #item does not have this info
		return -1, -1

	one_hot_dict = content.get_one_hot_dict()
	for item_id, rating in user_dict.items():
		sim = cos_items(item, item_id, content)
		plot_rating += rating * sim
		plot_sim += abs(sim)

		sim = cossine_call(one_hot_dict[item_id], one_hot_dict[item])
		genre_rating += rating * sim
		genre_sim += abs(sim)
	
	plot_rating = plot_rating/plot_sim if plot_sim != 0 else 0 
	genre_rating = genre_rating/genre_sim if genre_sim != 0 else 0

	return plot_rating, genre_rating

def genres_profile_calculation(genres_profile, start_perc=0.2):

	#genres_profile = genres_profile/np.linalg.norm(genres_profile)
	
	if start_perc > 0:
		qtd_genres = len(genres_profile)
		non_zero = np.array([1]*qtd_genres)
		#non_zero = non_zero/np.linalg.norm(non_zero)
		#print(non_zero)
		genres_profile = start_perc*non_zero + (1-start_perc)*genres_profile
		#print(2, genres_profile)
	
	return genres_profile

def generate_profile(user_dict, content, start_perc=0.2):

	one_hot_dict = content.get_one_hot_dict()
	genres_profile = np.array([0]*len(genre_list()))

	for item_id, rating in user_dict.items():
		genres_profile += rating*one_hot_dict[item_id]
		#plot_profile += rating*make_plot_vector(item_id, content)

	#print(1, genres_profile)
	
	genres_profile = genres_profile_calculation(genres_profile, start_perc)

	return genres_profile

# ---------- Plot calculations -------

def make_plot_vector(item, content):
	tf_idf = content.get_item_tfidf_dict(item)
	tf_idf = content.make_vector_from_tfidf(tf_idf)
	return tf_idf

# ---------- Wrapper for tests -------

def pass_this(content_dict):
	#get_unique_from_list(content_dict, col='Genre')

	
	genre_list = ['Action', 'Thriller']
	print(genre_one_hot(genre_list))

	for itemId, dicio in content_dict.items():
		#print(genre_one_hot(dicio['Genre']))

		if type(dicio['Plot']) == str:
			a = tokenizer.tokenize(dicio['Plot'])
			#print(a)


if __name__ == '__main__':
	from functools import partial
	from timer import time_a_function, compare_many_functions

	a = 1
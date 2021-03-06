#import time
import numpy as np
import pandas as pd

from collections import defaultdict
from setup import Setup
from content_func import Content, generate_profile, short_array_cos_sim, genres_avg_user, similarity_calculations

class Dados(object):
	'''
		Classe que guarda informações do dataframe
	'''
	def __init__(self, df):
		self.users = list(df['UserId'].unique())
		self.items = list(df['ItemId'].unique())
		self.dicio = self.set_dict(df)
	
	def set_dict(self, df):
		dicio = defaultdict(dict)
		users, items, ratings = df.values.T
		for u,i,r in zip(users, items, ratings):
			dicio[u][i] = r
		return dicio

	def get_users(self):
		return self.users

	def get_n_users(self):
		return len(self.users)
	
	def get_items(self):
		return self.items

	def get_n_items(self):
		return len(self.items)

	def get_dicio(self):
		return self.dicio

	def get_N_dicio(self):
		return len(self.dicio)

	def cleanup_results(self):
		#del self.tuples
		pass

def target_to_list(df):
	return [x for x in df.to_records(index=False)]

def set_enviromment(df, content_dict, set_up):
	'''
		Sets enviromment to work with
	'''
	dados = Dados(df)
	content = Content(content_dict)

	#verbose, tokenization, drop_list = set_up.get()

	return dados, content

def print_predictions(test_tuple, predictions):
	assert len(test_tuple) == len(predictions)

	print("UserId:ItemId,Prediction")
	for i in range(len(test_tuple)):
		print("{}:{},{}".format(test_tuple[i][0], test_tuple[i][1], predictions[i]))
	return

def get_item_avg(item_avg_rating, item_w_avg_rating):
	'''
		Returns mean of imdbRating and weighted rating
	'''
	if item_w_avg_rating == 0:
		return item_avg_rating
	return np.mean([item_avg_rating, item_w_avg_rating])

def overall_bias(user_dict, content):
	'''
		Calculates bias based on avg
	'''
	avg_rating = content.get_avg_rating()
	user_avg_rating = get_user_avg(user_dict)
	bruto = user_avg_rating - avg_rating
	percentual = (user_avg_rating - avg_rating)/avg_rating
	return bruto, percentual

def overall_weighted_bias(user_dict, content):
	'''
		Calculates bias based on weighted avg
	'''
	avg_rating = content.get_avg_weight_rating()
	user_avg_rating = get_user_avg(user_dict)
	bruto = user_avg_rating - avg_rating
	percentual = (user_avg_rating - avg_rating)/avg_rating
	return bruto, percentual

def genre_bias(user_dict, content):
	one_hot_dict = content.get_one_hot_dict()
	avg_user_genre = genres_avg_user(user_dict, one_hot_dict)
	return

def calculate_user_bias(user_dict, content_dict, column='imdbRating'):
	
	bruto, percentual, count = 0, 0, 0
	for item, rating in user_dict.items():
		imdbRating = content_dict[item][column]
		if imdbRating != 0:
			bruto += rating - imdbRating
			percentual += (rating - imdbRating)/imdbRating
			count += 1
	
	bruto = bruto/count
	percentual = percentual/count
	return bruto, percentual

def get_user_avg(user_dict):
	'''
		Returns the user mean rating
	'''
	user_avg_rating = sum(user_dict.values())/len(user_dict)
	return user_avg_rating

def item_rating_after_bias(item, user_dict, content_dict, content, perc=True):
	
	user_avg_rating = get_user_avg(user_dict)
	item_avg_rating = content.get_content_dict_item(item, col='imdbRating')
	item_w_avg_rating = content.get_content_dict_item(item, col='weighted_rate')
	
	bruto, percentual = calculate_user_bias(user_dict, content_dict, column='imdbRating')
	w_bruto, w_percentual = calculate_user_bias(user_dict, content_dict, column='weighted_rate')

	avg_after, w_avg_after = 0,0
	if perc:
		avg_after =  item_avg_rating * (1 + percentual)
		w_avg_after = item_w_avg_rating *(1 + w_percentual)
	else:
		avg_after = item_avg_rating + bruto
		w_avg_after = item_w_avg_rating + w_bruto
	
	if item_w_avg_rating == 0:
		return avg_after

	return np.mean([avg_after, w_avg_after])


def reset_weights(ratings_dict, weights=np.array([1/5, 1/5, 1/5, 1/5, 1/5])):
	
	plot_rating = ratings_dict['plot_rating']
	genre_rating = ratings_dict['genre_rating']
	year_rating = ratings_dict['year_rating']
	
	item_avg = get_item_avg(ratings_dict['imdbRating'], ratings_dict['weighted_rate'])
	item_after_bias = ratings_dict['item_after_bias'] if ratings_dict['item_after_bias']>0 else ratings_dict['weighted_rate']
	
	if plot_rating == -1: #does not have
		weights[3] = 0
		plot_rating = 0
	if genre_rating == -1: #does not have
		weights[4] = 0
		genre_rating = 0
	if year_rating == -1: #does not have
		weights[5]=0
		year_rating = 0
	'''
	tipo=''
	if ratings_dict['user_avg_rating'] == 0:
		tipo += "user_avg_rating | "
	if plot_rating == 0:
		tipo += "plot_rating | "
	if genre_rating == 0:
		tipo += "genre_rating"
	'''

	vector = [ratings_dict['user_avg_rating'], item_avg, item_after_bias, plot_rating, genre_rating, year_rating]
	pred = np.average(vector, weights=weights)

	return pred

def user_and_item(user_dict, item, content, perc=True, weights=np.array([1/5, 1/5, 1/5, 1/5, 1/5])):
	

	content_dict, one_hot_dict = content.get_content_dict(), content.get_one_hot_dict()
	ratings_dict = {
		'user_avg_rating':get_user_avg(user_dict),
		'weighted_rate': content.get_content_dict_item(item, col='weighted_rate'),
		'imdbRating': content.get_content_dict_item(item, col='imdbRating'),
		'item_after_bias': item_rating_after_bias(item, user_dict, content_dict, content, perc=perc)
		}

	plot_rating, genre_rating, year_rating = similarity_calculations(item, user_dict, content, start_perc=0.2)
	ratings_dict['plot_rating'] = plot_rating
	ratings_dict['genre_rating'] = genre_rating
	ratings_dict['year_rating'] = year_rating

	#print(item, plot_rating, genre_rating)
	pred = reset_weights(ratings_dict, weights=weights)
	return pred

def user_not_item(user_dict, content, perc=True, show=False):
	
	content_dict, one_hot_dict = content.get_content_dict(), content.get_one_hot_dict()


	bruto, percentual = calculate_user_bias(user_dict, content_dict, column='imdbRating')
	w_bruto, w_percentual = calculate_user_bias(user_dict, content_dict, column='weighted_rate')

	avg_rating = content.get_avg_rating()
	avg_w_rating = content.get_avg_weight_rating()

	if show:
		for item, rating in user_dict.items():
			imdbRating = content_dict[item]['imdbRating']
			b = imdbRating + bruto
			p = imdbRating * (1+percentual)
			print("Rating: {} | imdbRating: {} | bruto: {} | perc: {}".format(rating, imdbRating, b, p))

	#genres_avg_user(user_dict, one_hot_dict)

	avg_after, w_avg_after = 0,0
	if perc:
		avg_after =  avg_rating * (1 + percentual)
		w_avg_after = avg_w_rating *(1 + w_percentual)
	else:
		avg_after = avg_rating + bruto
		w_avg_after = avg_w_rating + w_bruto
	
	return np.mean([avg_after, w_avg_after])
	
def item_category_avg(item, content, category='Genre'):
	if category == 'Genre':
		genre_avg = content.get_movie_avg_genre_rating(content.get_content_dict_item(item, 'Genre'))
		return genre_avg
	if category == 'Decade':
		decade_avg = content.get_movie_avg_decade_rating(content.get_content_dict_item(item, 'Decade'))
		return decade_avg
	return 0

def item_not_user(item, content):
	
	pred = 0
	avg_rating = np.mean([content.get_avg_rating(), content.get_avg_weight_rating()])

	content_dict = content.get_content_dict()

	if content_dict[item]['imdbRating'] == 0:
		weights = [6/8, 1.5/8, 0.5/8] #avg, genre, decade
		genre_avg = item_category_avg(item, content, category='Genre')
		decade_avg = item_category_avg(item, content, category='Decade')
		if len(content_dict[item]['Genre']) == 0:
			weights[1] = 0
		if content_dict[item]['Decade'] == 0:
			weights[2] = 0
		pred = np.average([avg_rating, genre_avg, decade_avg], weights=weights)

	elif content_dict[item]['weighted_rate'] == 0:
		weights = [0.05, 0.8, 0.1, 0.05] #avg, item_avg, genre, decade
		item_avg = content_dict[item]['imdbRating']
		genre_avg = item_category_avg(item, content, category='Genre')
		decade_avg = item_category_avg(item, content, category='Decade')
		
		if len(content_dict[item]['Genre']) == 0:
			weights[2] = 0
			weights[0] = 0.1
			weights[1] = 0.9
		if content_dict[item]['Decade'] == 0:
			weights[3] = 0
		pred = np.average([avg_rating, item_avg, genre_avg, decade_avg], weights=weights)
	
	else:
		weights = [0.05, 0.9, 0.05, 0] #avg, item_avg, genre, decade
		item_avg = content_dict[item]['imdbRating']
		w_avg = content_dict[item]['weighted_rate']
		item_avg = np.mean([item_avg, w_avg])

		genre_avg = item_category_avg(item, content, category='Genre')
		decade_avg = item_category_avg(item, content, category='Decade')
		
		if len(content_dict[item]['Genre']) == 0:
			weights[2] = 0
			weights[1] = 0.95
		if content_dict[item]['Decade'] == 0:
			weights[3] = 0
		pred = np.average([avg_rating, item_avg, genre_avg, decade_avg], weights=weights)

	return pred

def get_predictions(in_, dados, content, set_up):
	
	verbose, tokenization, drop_list, weights, perc = set_up.get()

	test_tuple = target_to_list(in_)
	predictions = []

	#input related
	dicio = dados.get_dicio()
	users_d = dict.fromkeys(dados.get_users(), 0)
	items_d = dict.fromkeys(dados.get_items(), 0)
	
	#content related
	avg_rating = content.get_avg_rating()
	mean_rating = content.get_mean_rating()
	w_avg_rating = content.get_avg_weight_rating()
	w_mean_rating = content.get_mean_weight_rating()


	pred = 0

	#w = [ratings_dict['user_avg_rating'], item_avg, item_after_bias, plot_rating, genre_rating, year_rating]
	#weights=np.array([1/20, 0, 10/20, 4/20, 3/20, 2/20]) out 21
	#weights=np.array([1/20, 1/20, 9/20, 3/20, 4/20, 2/20]) out 27
	#weights=np.array([1/20, 5/20, 5/20, 3/20, 4/20, 2/20]) out 30
	#weights=np.array([3/40, 11/40, 10/40, 6/40, 7/40, 3/40])

	for user, item in test_tuple:
		#both were in train
		if user in users_d and item in items_d:
			#print(dicio[user])
			pred = user_and_item(dicio[user], item, content, perc=perc, weights=weights)
		
		#only user in train
		elif user in users_d:
			pred = user_not_item(dicio[user], content)

		#only item in train
		elif item in items_d:
			pred = item_not_user(item, content)

		#frozen
		else:
			pred = np.mean([w_avg_rating, avg_rating])
		
		#sanity check
		pred = 10 if pred>10 else pred
		pred = 0 if pred < 0 else pred
		predictions.append(pred)
		
	print_predictions(test_tuple, predictions)
	return
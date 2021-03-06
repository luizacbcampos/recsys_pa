#import time
import re
import sys
import numpy as np
import pandas as pd

#meus
import ratings_func as rf
from setup import Setup


from content_func import pass_this
from read_content import load_content
from tokenizer import create_word_set_and_dict, computeTF, computeIDF, create_TFIDF_dict, create_TFIDF

from timer import time_a_function, compare_many_functions
from functools import partial


ratings_file ="ratings.csv"
targets_file = "targets.csv"
content_file = "content.csv"

if len(sys.argv) > 3:
	content_file = sys.argv[1]
	ratings_file = sys.argv[2]
	targets_file = sys.argv[3]

#---------------- Auxiliary functions ----------------------

def print_list(lista):
	'''
		Prints full list
	'''
	for w in lista:
		print(w)

def non_zero_dict(dicio):
	return {k: v for k, v in dicio.items() if v != 0}

#---------------- Loading functions ----------------------

def load_ratings(ratings_file):
	'''
		Loads the ratings file
	'''
	df = pd.read_csv(ratings_file, usecols=[0,1], dtype={"UserId:ItemId":"string", "Prediction": "int8"})
	df[['UserId','ItemId']] = df['UserId:ItemId'].str.split(':',expand=True)
	df = df.drop(columns=['UserId:ItemId'])
	return df[['UserId','ItemId', 'Prediction']]

def load_targets(targets_file):
	'''
		Loads the targets_file
	'''
	return pd.read_csv(targets_file, sep=':', dtype={"UserId": "string", "ItemId": "string"})


#---------------- Main ----------------------

df = load_ratings(ratings_file)

drops = ['Rated', 'Released', 'Runtime', 'Director', 'Writer', 'Actors', 'Language', 'Country', 'Awards', 
		'Poster', 'Metascore', 'imdbID', 'Type', 'Response', 'Error', 'Season', 'Episode', 'seriesID']

#w = [ratings_dict['user_avg_rating'], item_avg, item_after_bias, plot_rating, genre_rating, year_rating]
w = np.array([0/40, 9/40, 14/40, 7/40, 7/40, 3/40])
#w = np.array([1/40, 12/40, 10/40, 7/40, 7/40, 3/40])

set_up = Setup(verbose=False, lower_=True, number=True, apostrophe=True, punctuation=True, 
	stem='snowball', accents=True, drop_list=drops, weights=w, perc=True)

content_dict = load_content(content_file, drop_list=set_up.get_drop_list())

#time_a_function(rf.set_enviromment, df, content_dict, set_up)
dados, content = rf.set_enviromment(df, content_dict, set_up)

t = load_targets(targets_file)

rf.get_predictions(t, dados, content, set_up)

#time_a_function(rf.get_predictions, t, dados, content, set_up)





#pass_this(content_dict)

'''
print("lower_=True, number=True")
wordSet, token_dict = create_word_set_and_dict(content_dict, lower_=True, number=True)
print(len(wordSet))
#print_list(wordSet)
idfDict = computeIDF(wordSet, token_dict)
create_TFIDF_dict(wordSet, token_dict, idfDict)

#print(non_zero_dict(tfidf))
'''

'''
compare_many_functions([partial(create_word_set,content_dict), partial(create_word_set,content_dict, lower_=True, number=False)], 10)
'''
#import time
import re
import sys
import numpy as np
import pandas as pd

#meus
#import matrix as m

import json #speed test
from timer import time_a_function, compare_functions
from functools import partial
from ast import literal_eval


ratings_file ="ratings.csv"
targets_file = "targets.csv"
content_file = "content.csv"

if len(sys.argv) > 3:
	ratings_file = sys.argv[1]
	targets_file = sys.argv[2]
	content_file = sys.argv[3]


#---------------- Auxiliary functions ----------------------

def print_full(x):
	'''
		Prints dataframe in full
	'''
	pd.set_option('display.max_rows', len(x))
	print(x)
	pd.reset_option('display.max_rows')


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


def load_content(content_file):


	def possible_drops():
		'''
		df['Response'] = just one | df['Error'] = just one 
		df['Poster'] = useless | df['imdbID'] = not relevant
		df['Episode'] = 1 value only | df['seriesID'] = 1 value only
		df['Type'] = mostly movies | df['Metascore'] = few values
		'''
		col = ['ItemId', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre','Director', 'Writer',
			'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating',
			'imdbVotes', 'imdbID', 'Type', 'Response', 'Error', 'Season', 'Episode', 'seriesID']
		
		drops = ['Response', 'Error', 'Type', 'Poster', 'Episode', 'Season', 'seriesID', 'Metascore', 'imdbID']
		return drops

	def make_list_dict(content_file):
		dicio_list = [] 
		f = open(content_file, 'r')
		next(f)
		for line in f.readlines():
			itemId, json_string = line.split(',', 1)
			json_dicio = {'ItemId': itemId}
			json_dicio.update(literal_eval(json_string))
			dicio_list.append(json_dicio)
		f.close()
		return dicio_list

	def data_cleaning(df):
		def replace_value(col, value, replace=np.nan):
			return np.where((df[col] == value),replace,df[col])

		def convert_to_minutes(col):
			def str_to_min(x):
				if pd.isnull(x['Runtime']):
					return x['Runtime']
				else:
					l = x['Runtime'].split('h')
					if len(l) == 2:
						hour = int(l[0])
						minute = int(l[1].split(' ')[1])
						return hour*60 + minute
					else:
						minute = int(l[0].split(' ')[0])
						return minute
			#df[col] = df.apply(lambda x: str_to_min(x), axis=1)
			return df.apply(lambda x: str_to_min(x), axis=1)
		
		def age_rating(col):
			
			df[col] = df[col].str.lower()
			nans = ['not rated', 'unrated']
			for value in nans:
				df[col] = replace_value(col, value)
			
			return df[col]
		

		df = df.replace(to_replace=r'^N/A$', value=np.nan, regex=True)
		
		df['Runtime'] = convert_to_minutes('Runtime')
		df['Rated'] = age_rating('Rated')
		return df

	content_dict = make_list_dict(content_file)	
	df = pd.DataFrame.from_records(content_dict, exclude=possible_drops())
	
	print(df['Director'].value_counts())
	print(df.columns)
	df = data_cleaning(df)
	print_full(df['Rated'].value_counts())
	print(df)

print("-----------------------------------------------")


df = load_ratings(ratings_file)
load_content(content_file)

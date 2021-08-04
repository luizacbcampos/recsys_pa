#import time
import re
import sys
import numpy as np
import pandas as pd
from ast import literal_eval
from datetime import datetime


#---------------- Auxiliary functions ----------------------

def print_full(x):
	'''
		Prints dataframe in full
	'''
	pd.set_option('display.max_rows', len(x))
	print(x)
	pd.reset_option('display.max_rows')

# ---------- Category selecting --------------------

def all_categories():
	'''
		All possible json keys
	'''
	col = ['ItemId', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre','Director', 'Writer',
		'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating',
		'imdbVotes', 'imdbID', 'Type', 'Response', 'Error', 'Season', 'Episode', 'seriesID']
	return col

def possible_drops(drop_list=None):
	'''
	df['Response'] = just one | df['Error'] = just one 
	df['Poster'] = useless | df['imdbID'] = not relevant
	df['Episode'] = 1 value only | df['seriesID'] = 1 value only
	df['Type'] = mostly movies | df['Metascore'] = few values
	'''
	if drop_list == None:
		drops = ['Response', 'Error', 'Type', 'Poster', 'Episode', 'Season', 'seriesID', 'Metascore', 'imdbID']
		return drops
	return drop_list

def category_keeps(drop_list=None):
	'''
		Categories kept
	'''
	x = all_categories()
	y = possible_drops(drop_list)
	return [item for item in x if item not in y]

def make_dict(drop_list=None):
	'''
		Initial dict based on kept columns. To sum dicts: dicio = {**x, **y} 
	'''
	return {k: 'N/A' for k in category_keeps(drop_list)}


# ------------ Dict cleaning ---------------------------

def dicio_type_check(dicio_list, row=128):
	
	for a in dicio_list[row].keys():
		print(a, type(dicio_list[row][a]))
	return

def loadable_json(content):
	'''
		Converts json so its readable by json.loads
	'''
	return content.replace('"',  r'\"').replace('{', '"{').replace('}', '}"')

def drop_columns(json_dicio, drop_list=None):
	'''
		Drops columns based on possible_drops()
	'''
	for drop in possible_drops(drop_list):
		json_dicio.pop(drop, None)
	return json_dicio

def replace_str(some_dict, string=r'^N/A$', replace=np.nan):
	'''
		Replaces string on the dict
	'''
	return { k: (replace if re.match(string,v) else v) for k, v in some_dict.items() }

def convert_to_minutes(json_dicio):
	'''
		Fixes the 'Runtime'
	'''
	l = json_dicio['Runtime'].split('h')
	if len(l) == 2:
		hour = int(l[0])
		minute = int(l[1].split(' ')[1])
		json_dicio['Runtime'] = hour*60 + minute
	else:
		minute = int(l[0].split(' ')[0])
		json_dicio['Runtime'] = minute
	return json_dicio

def released_to_datetime(json_dicio):
	'''
		Converts string to datetime
	'''
	# i check if it's not null before
	json_dicio['Released'] = datetime.strptime(json_dicio['Released'], '%d %b %Y')
	#datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
	return json_dicio

def age_rating(json_dicio):
	'''
		Fixes the ratings
	'''
	json_dicio['Rated'] = json_dicio['Rated'].lower() if type(json_dicio['Rated']) == str else json_dicio['Rated']
	nans = ['not rated', 'unrated']
	if json_dicio['Rated'] in nans:
		json_dicio['Rated'] = np.nan
	return json_dicio

def convert_to_number(json_dicio, col='imdbRating', numeric_type=float):
	'''
		Converts a category to numeric. Float is default
	'''
	# i check if it's not null before
	json_dicio[col] = numeric_type(json_dicio[col])
	return json_dicio

def split_to_list(json_dicio, col='Genre', sep=", "):
	'''
		Converts a category to list.
	'''
	# i check if it's not null before
	json_dicio[col] = json_dicio[col].split(sep)
	return json_dicio

def writers_split(json_dicio, sep=", "):
	'''
		Converts the writer's column
	'''
	
	writers_list = json_dicio['Writer'].split(sep)
	w = {'name': list(), 'function':list()}
	for writer in writers_list:
		first, last = writer.find(" ("), writer.find(")")
		person = writer if first == -1 else writer[0:first]
		function = 'writer' if first==-1 else writer[first+2:last]
		w['name'].append(person)
		w['function'].append(function.lower())

	json_dicio['Writer'] = w
	return json_dicio

def awards_split(json_dicio):
	'''
		Converts the awards column
	'''
	def replace_for_value(lista):
		if len(lista) == 0:
			return 0
		#len(lista) == 1
		return int(lista[0].split(' ')[0])

	def update(dicio, entry, entry_name):
		replacement_dict = {'BAFTA Film Award': 'BAFTA', 'BAFTA Film Awards': 'BAFTA', 'Golden Globe':'Golden Globe',
		'Golden Globes':'Golden Globe', 'Oscar':'Oscar', 'Oscars':'Oscar', 'Primetime Emmy':'Emmy', 'Primetime Emmys':'Emmy'}

		if type(entry) == list:
			dicio[replacement_dict[entry[1]]] = {entry_name: int(entry[0])}
			dicio[entry_name] += int(entry[0])
		return dicio

	def specific_awards(lista, dicio):
		
		if len(lista) == 0:
			return dicio

		noms = re.findall(r'(?<=Nominated for ).*', lista[0])
		wins = re.findall(r'(?<=Won ).*',  lista[0])

		noms = noms[0].split(' ', 1) if len(noms)== 1 else 0
		wins = wins[0].split(' ', 1) if len(wins)== 1 else 0
		
		dicio = update(dicio, entry=noms, entry_name='nomination')
		dicio = update(dicio, entry=wins, entry_name='win')
		return dicio

	# i check if it's not null before
	result = {}
	result['win'] = replace_for_value(re.findall(r'[\d]+ win[s]*', json_dicio['Awards']))
	result['nomination'] = replace_for_value(re.findall(r'[\d]+ nomination[s]*', json_dicio['Awards']))
	json_dicio['Awards'] = specific_awards(json_dicio['Awards'].split('.', 1), result)

	return json_dicio


def data_cleaning(json_dicio, columns_keep, drop_list=None):
	'''
		Cleans the dict
	'''
	json_dicio = drop_columns(json_dicio, drop_list)
	json_dicio = replace_str(json_dicio)
	
	for col in columns_keep:
		if pd.notnull(json_dicio[col]):
			if col == 'Runtime':
				json_dicio = convert_to_minutes(json_dicio)

			elif col == 'Rated':
				json_dicio = age_rating(json_dicio)

			elif col == 'imdbRating':
				json_dicio = convert_to_number(json_dicio, col, numeric_type=float)

			elif col == 'Year':
				json_dicio = convert_to_number(json_dicio, col, numeric_type=int)

			elif col == 'imdbVotes':
				json_dicio[col] = int(json_dicio[col].replace(",", ""))

			elif col == 'Genre':
				json_dicio = split_to_list(json_dicio, col)

			elif col == 'Director':
				json_dicio = split_to_list(json_dicio, col)

			elif col == 'Language':
				json_dicio[col] = json_dicio[col].replace("Norse,  Old", "Old Norse") #corrects a mistake
				json_dicio = split_to_list(json_dicio, col)
				#pass
			elif col == 'Country':
				json_dicio = split_to_list(json_dicio, col)

			elif col == 'Actors':
				json_dicio = split_to_list(json_dicio, col)

			elif col == 'Writer':
				#json_dicio = split_to_list(json_dicio, col) #look after
				json_dicio = writers_split(json_dicio, sep=", ")
			elif col == 'Awards':
				json_dicio = awards_split(json_dicio)

			elif col == 'Released':
				json_dicio = released_to_datetime(json_dicio)
				#pass
			
		#print(col)
	return json_dicio

def load_content(content_file="content.csv", drop_list=None):
	'''
		Loads the csv
	'''
	def make_list_dict(content_file):
		
		dicio_list = [] 
		f = open(content_file, 'r')
		y = make_dict(drop_list)
		columns_keep = category_keeps(drop_list)
		next(f)
		
		for line in f.readlines():
			itemId, json_string = line.split(',', 1)
			json_dicio = {**y, **{'ItemId': itemId}}
			json_dicio.update(literal_eval(json_string))
			#modifications
			json_dicio = data_cleaning(json_dicio, columns_keep, drop_list)
			dicio_list.append(json_dicio)

		f.close()
		return dicio_list

	return make_list_dict(content_file)


def main(content_file="content.csv", drop_list=None, pandas=False, verbose=False):

	content_dict = load_content(content_file, drop_list)
	
	if verbose:
		dicio_type_check(content_dict, row=128)

	if pandas:
		df = pd.DataFrame.from_records(content_dict, exclude=['Genre','Director','Writer','Actors','Language', 'Country', 'Awards'])
		print(df['Title'].value_counts())
		print(df.columns)

		#print(df.loc[df['Writer'] == 'Anders Nyberg, Ola Olsson, Carin Pollak, Kay Pollak, Margaretha Pollak'])
		#print_full(df['Director'].value_counts())
		#print(df)
		print(df.dtypes)
	return content_dict

if __name__ == '__main__':
	
	from functools import partial
	from timer import time_a_function, compare_functions
	
	content_file = "content.csv"

	drops = ['Response', 'Error', 'Type', 'Poster', 'Episode', 'Season', 'seriesID', 'Metascore', 'imdbID']
	main(content_file, drops, pandas=True, verbose=True)


	#compare_functions(partial(load_content, content_file), partial(load_content, content_file, on_dict=False), 10)
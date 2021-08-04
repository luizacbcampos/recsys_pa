import time
import numpy as np
import pandas as pd
from functools import partial

# --- MACROS

ratings_file="ratings.csv"
targets_file = "targets.csv"
content_file = "content.csv"

# --- FUNCTIONS

def convert(val):
	return tuple(val.split(":"))

def load_ratings(ratings_file, date=False):
	if date:
		df = pd.read_csv(ratings_file, converters={"UserId:ItemId": convert}, dtype={"Prediction": "int8"})
	else:
		df = pd.read_csv(ratings_file, usecols=[0,1], converters={"UserId:ItemId": convert}, dtype={"Prediction": "int8"})

def load_targets(targets_file):
	return pd.read_csv(targets_file, sep=':', dtype={"UserId": "string", "ItemId": "string"})

def time_a_function(func, *args, verbose=True):
	'''
		Time a function
	'''
	start_time = time.time()
	func(*args)
	time_run = time.time() - start_time
	if verbose:
		print("--- %s : %s seconds ---" % (str(func).split(" ")[1], time_run))
	return time_run

def compare_functions(one, two, runs=20):
	'''
		Times two functions
	'''
	a, b = 0,0
	for i in range(runs):
		a += time_a_function(one, verbose=False)
		b += time_a_function(two, verbose=False)
	print("{} = {} & {} = {}".format(str(one).split(" ")[1], a/runs, str(two).split(" ")[1], b/runs))
	return a/runs, b/runs


def compare_many_functions(fun_list, runs=20):
	'''
		Times all functions in fun_list
	'''
	times = [0 for i in range(len(fun_list))]
	for i in range(runs):
		for j in range(len(fun_list)):
			times[j] += time_a_function(fun_list[j], verbose=False)
	
	for j in range(len(fun_list)):
		print("{} = {}".format(str(fun_list[j]).split(" ")[1], times[j]/runs))


if __name__ == '__main__':
	time_a_function(load_targets, targets_file)


	time_a_function(load_ratings, ratings_file)
	
	#compare_many_functions(fun_list, runs=20)

	compare_many_functions([partial(load_targets, targets_file), partial(load_ratings, ratings_file)], 10)

	#1
	from datetime import datetime
	datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

	print(datetime_object, type(datetime_object))
	
	'''
	start_time = time.time()
	df = pd.read_csv(targets_file, converters={"UserId:ItemId": convert})
	print("--- %s seconds ---" % (time.time() - start_time))
	print(df)


	start_time = time.time()
	df = load_targets(targets_file)
	print("--- %s seconds ---" % (time.time() - start_time))
	print(df)
	'''
	
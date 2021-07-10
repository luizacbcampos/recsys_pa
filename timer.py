import time
import numpy as np
import pandas as pd

# --- MACROS

ratings_file="ratings.csv"
targets_file = "targets.csv"

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

def time_a_function(func, *args):
	start_time = time.time()
	func(*args)
	print("--- %s : %s seconds ---" % (str(func).split(" ")[1], time.time() - start_time))

if __name__ == '__main__':
	time_a_function(load_targets, targets_file)


	time_a_function(load_ratings, ratings_file)
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
	
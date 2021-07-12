#import time
import sys
import numpy as np
import pandas as pd

#meus
import matrix as m



ratings_file ="ratings.csv"
targets_file = "targets.csv"

if len(sys.argv) > 2:
	ratings_file = sys.argv[1]
	targets_file = sys.argv[2]



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


df = load_ratings(ratings_file)


set_up = m.setup(k=15, epochs=13, l_rt=0.009, reg=0.1, random=False, verbose=True)
dados = m.set_enviromment(df, set_up)

t = load_targets(targets_file)
m.get_predictions(t, dados, set_up)


'''
start_time = time.time()
df = load_targets(targets_file)
print("--- %s seconds ---" % (time.time() - start_time))
print(df)

'''
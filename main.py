import time
import numpy as np
import pandas as pd

from timer import time_a_function
import matrix as m

ratings_file="ratings.csv"
targets_file = "targets.csv"


def convert(val):
	return tuple(val.split(":"))

def load_ratings(ratings_file, date=False):
	if date:
		return pd.read_csv(ratings_file, converters={"UserId:ItemId": convert}, dtype={"Prediction": "int8"})
	else:
		#df = pd.read_csv(ratings_file, usecols=[0,1], converters={"UserId:ItemId": convert}, dtype={"Prediction": "int8"})
		df = pd.read_csv(ratings_file, usecols=[0,1], dtype={"UserId:ItemId":"string", "Prediction": "int8"})
		df[['UserId','ItemId']] = df['UserId:ItemId'].str.split(':',expand=True)
		df = df.drop(columns=['UserId:ItemId'])
		return df[['UserId','ItemId', 'Prediction']]

def load_targets(targets_file):
	return pd.read_csv(targets_file, sep=':', dtype={"UserId": "string", "ItemId": "string"})


#time_a_function(load_ratings, ratings_file)


df = load_ratings(ratings_file)

a = df.groupby(by='UserId', observed=True, sort=False)['Prediction'].agg(['count','mean']).to_numpy()
print(a[0,1])

#'u0020931'

m.set_enviromment(df, k=20, epochs=1, random=False)
#dados = m.Dados(df)


#print(dados.get_users())

t = load_targets(targets_file)


#m.create_utility_matrix(df)

'''
start_time = time.time()
df = pd.read_csv(ratings_file, usecols=[0,1], converters={"UserId:ItemId": convert}, dtype={"Prediction": "int8"})
print("--- %s seconds ---" % (time.time() - start_time))

print(df)


start_time = time.time()
df = pd.read_csv(targets_file, converters={"UserId:ItemId": convert})
print("--- %s seconds ---" % (time.time() - start_time))
print(df)


start_time = time.time()
df = load_targets(targets_file)
print("--- %s seconds ---" % (time.time() - start_time))
print(df)

'''
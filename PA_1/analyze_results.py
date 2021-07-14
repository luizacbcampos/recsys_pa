import numpy as np
import pandas as pd

results = "results.csv"

df = pd.read_csv(results)

def same_run(df):
	grouped = df.groupby(['epoch','k','alpha','lamda'])
	for name, group in grouped:
		print(" * epoch = {}, k = {}, alpha = {}, lambda = {}".format(name[0], name[1], name[2], name[3]))
		print(group)

def rank_runs(df):
	print(df.sort_values(by=['RMSE']))
#same_run(df)
rank_runs(df)

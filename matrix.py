import time
import numpy as np
import pandas as pd

class Dados:
	'''
		Classe que guarda informações do dataframe
	'''
	def __init__(self, df):
		self.users = list(df['UserId'].unique())
		self.items = list(df['ItemId'].unique())
		#dicionarios
		self.users_dict = {self.users[i]: i for i in range(len(self.users))}
		self.items_dict = {self.items[i]: i for i in range(len(self.items))}
		#tupla
		self.tuples = [(self.users_dict[x[0]], self.items_dict[x[1]], x[2]) for x in df.to_records(index=False)]

		#info
		# np.array [count, mean]
		self.mu = df['Prediction'].mean()
		self.users_avg = df.groupby(by='UserId', observed=True, sort=False)['Prediction'].agg(['count','mean']).to_numpy()
		self.items_avg = df.groupby(by='ItemId', observed=True, sort=False)['Prediction'].agg(['count','mean']).to_numpy()
	
	def get_users(self):
		return self.users

	def get_n_users(self):
		return len(self.users)
	
	def get_items(self):
		return self.items

	def get_n_items(self):
		return len(self.items)

	def get_users_dict(self):
		return self.users_dict

	def get_items_dict(self):
		return self.items_dict
	
	def get_tuples(self):
		return self.tuples

	def get_N_tuples(self):
		return len(self.tuples)
	
	def get_user_number(self, u):
		return self.users_dict[u]

	def get_item_number(self, i):
		return self.items_dict[i]

	def get_mu(self):
		return self.mu

	def get_users_avg(self):
		return self.users_avg[:,1]

	def get_items_avg(self):
		return self.items_avg[:,1]

	def get_user_avg(self, u): #u is a NUMBER
		return self.users_avg[u,1]
	
	def get_item_avg(self, i): #i is a NUMBER
		return self.items_avg[i,1]

	def algo(self, u, k):
		tuple_emb = list(filter(lambda x: x[0]==u, self.get_tuples()))
		u_emb = [x[2] for x in tuple_emb]
		return 0

def targets(df):

	def make_list(df):
		return [x for x in df.to_records(index=False)]
	pass

def get_bias(dados):
	
	global_bias = dados.get_mu()
	user_bias = np.reshape(dados.get_users_avg(), (-1,1))
	item_bias = np.reshape(dados.get_items_avg(), (-1,1))
	
	return global_bias, user_bias, item_bias

def create_embeddings(dados, k, random=False):
	'''
		O user e o item embbeding é aleatório numa primeira ida.
		Aqui há duas opções: Ones ou Random. Default é ones
	'''
	def set_with_ones():
		user_embedding = np.ones((dados.get_n_users(), k))
		item_embedding = np.ones((dados.get_n_items(), k))
		return user_embedding, item_embedding
	
	def set_with_random():
		user_embedding = np.random.random((dados.get_n_users(), k))/k
		item_embedding = np.random.random((dados.get_n_items(), k))/k
		return user_embedding, item_embedding

	if not random:
		user_embedding, item_embedding = set_with_ones()
	else:
		user_embedding, item_embedding = set_with_random()
	
	return user_embedding, item_embedding

def predict_r(user_embedding, item_embedding, global_bias, user_bias, item_bias):
	r_hat = np.dot(user_embedding, item_embedding.T) + global_bias + user_bias + item_bias
	return r_hat

def set_enviromment(df, k=20, epochs=5, learning_rate=0.00001, regularizer=0.000001, random=False):
	'''
		k = number of factors = embedding_size
	'''
	dados = Dados(df)

	#vector and matrix creation
	user_embedding, item_embedding = create_embeddings(dados, k, random)
	
	global_bias, user_bias, item_bias = get_bias(dados)
	
	dele = np.random.random((dados.get_n_items(), k))/k

	N = dados.get_N_tuples()

	def one_epoch(N, epoch=0, verbose=False):
		erro = 0

		for userIndex, itemIndex, r in dados.get_tuples():
			
			ui_dot = 0

			for f in range(k):
				ui_dot += user_embedding[userIndex,f]*item_features[itemIndex, f]
			r_hat = ui_dot + global_bias + user_bias[userIndex,0] + item_bias[itemIndex, 0]
			res = r - r_hat
			user_bias[userIndex, 0] += learning_rate * (res - regularizer * user_bias[userIndex,0])
			item_bias[itemIndex, 0] += learning_rate * (res - regularizer * item_bias[itemIndex,0])

			erro += res**2

			for f in range(k):
				user_embedding[userIndex, f] = learning_rate * (res * item_embedding[itemIndex, f] - regularizer* user_embedding[userIndex, f])
				item_embedding[itemIndex, f] = learning_rate * (res * user_embedding[userIndex, f] - regularizer* item_embedding[itemIndex, f])
		if verbose:
                erro = erro / N
                print("Epoch " + str(epoch) + ": Error: " + str(erro))
	
	for i in range(epochs):
		one_epoch(N, i, True)

	return 0
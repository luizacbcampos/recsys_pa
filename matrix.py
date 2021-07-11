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

		#Resultados
		self.user_embedding = None
		self.item_embedding = None
		self.user_bias = None
		self.item_bias = None

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

	def get_mu(self):
		return self.mu

	def get_users_avg(self):
		return self.users_avg[:,1] - self.mu

	def get_items_avg(self):
		return self.items_avg[:,1] - self.mu

	def set_u_emb(self, user_emb):
		self.user_embedding = user_emb

	def set_i_emb(self, item_emb):
		self.item_embedding = item_emb

	def get_embeddings(self):
		return self.user_embedding, self.item_embedding
	
	def set_u_bias(self, user_b):
		self.user_bias = user_b
	
	def set_i_bias(self, item_b):
		self.item_bias = item_b

	def get_bias(self):
		return self.user_bias, self.item_bias

	def cleanup_results(self):
		del self.users_avg
		del self.items_avg
		del self.tuples

class setup(object):
	""" Setup arguments class """
	def __init__(self, k, epochs, l_rt, reg, random, verbose):
		self.k = k
		self.epochs = epochs
		self.learning_rate = l_rt
		self.regularizer = reg
		self.random = random
		self.verbose = verbose
	def get(self):
		return self.k, self.epochs, self.learning_rate, self.regularizer, self.random, self.verbose
		


def target_to_list(df):
	return [x for x in df.to_records(index=False)]

def get_bias(dados):
	
	global_bias = dados.get_mu()
	user_bias = np.zeros((dados.get_n_users(), 1))
	item_bias = np.zeros((dados.get_n_items(), 1))

	'''
	This was causing ratings > 10. It was replaced

	user_bias = np.reshape(dados.get_users_avg(), (-1,1))
	item_bias = np.reshape(dados.get_items_avg(), (-1,1))
	'''

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

def set_enviromment(df, set_up):
	'''
		k = number of factors = embedding_size
	'''
	dados = Dados(df)
	k, epochs, learning_rate, regularizer, random, verbose = set_up.get()
	#vector and matrix creation
	user_embedding, item_embedding = create_embeddings(dados, k, random)
	
	global_bias, user_bias, item_bias = get_bias(dados)

	N = dados.get_N_tuples()

	dados_tuples = dados.get_tuples()
	
	if verbose:
		print("Running model with {} epochs k = {}, l_rt = {} and reg = {}".format(epochs, k, learning_rate, regularizer))

	def one_epoch(N, epoch=0, verbose=False):
		erro = 0

		for userIndex, itemIndex, r in dados_tuples:
			
			ui_dot = 0

			for f in range(k):
				ui_dot += user_embedding[userIndex,f]*item_embedding[itemIndex, f]
			
			r_hat = ui_dot + global_bias + user_bias[userIndex,0] + item_bias[itemIndex, 0]
			res = r - r_hat
			user_bias[userIndex, 0] += learning_rate * (res - regularizer * user_bias[userIndex,0])
			item_bias[itemIndex, 0] += learning_rate * (res - regularizer * item_bias[itemIndex,0])

			erro += res**2

			for f in range(k):
				#ATENÇÃO MUDEI AQUI: COLOQUEI O 2*L_RT
				user_embedding[userIndex, f] += 2*learning_rate * (res * item_embedding[itemIndex, f] - regularizer* user_embedding[userIndex, f])
				item_embedding[itemIndex, f] += 2*learning_rate * (res * user_embedding[userIndex, f] - regularizer* item_embedding[itemIndex, f])
		
		if verbose:
			erro = np.sqrt(erro / N)
			print("Epoch " + str(epoch) + ": Error: " + str(erro))
	
	for i in range(epochs):
		#start_time = time.time()
		one_epoch(N, i, True)
		#print("--- %s : %s seconds ---" % (str(i), time.time() - start_time))

	# Assign
	dados.set_u_emb(user_embedding)
	dados.set_i_emb(item_embedding)
	dados.set_u_bias(user_bias)
	dados.set_i_bias(item_bias)
	dados.cleanup_results()

	return dados

def print_predictions(test_tuple, predictions):
	assert len(test_tuple) == len(predictions)

	print("UserId:ItemId,Prediction")
	for i in range(len(test_tuple)):
		print("{}:{},{}".format(test_tuple[i][0], test_tuple[i][1], predictions[i]))
	return

def get_predictions(in_, dados, set_up):
	
	k, epochs, learning_rate, regularizer, random, verbose = set_up.get()
	test_tuple = target_to_list(in_)
	predictions = []

	#get dicts
	users_d = dados.get_users_dict()
	items_d = dados.get_items_dict()

	#get needed bias vectors
	global_bias = dados.get_mu()
	user_bias, item_bias = dados.get_bias()

	#get the matrixes
	user_embedding, item_embedding = dados.get_embeddings()
	#exit()
	for i in range(len(test_tuple)):
		user = test_tuple[i][0]
		item = test_tuple[i][1]

		#both were in train
		if user in users_d and item in items_d:
			userIndex = users_d[user]
			itemIndex = items_d[item]
			ui_dot = 0
			for f in range(k):
				ui_dot += user_embedding[userIndex, f] * item_embedding[itemIndex, f]
			
			pred = ui_dot + global_bias + user_bias[userIndex, 0] + item_bias[itemIndex, 0]
			predictions.append(pred)

		#only user in train
		elif user in users_d:
			predictions.append(global_bias + user_bias[users_d[user], 0])

		#only item in train
		elif item in items_d:
			predictions.append(global_bias + item_bias[items_d[item], 0])

		#frozen
		else:
			predictions.append(global_bias)

	print_predictions(test_tuple, predictions)
	return
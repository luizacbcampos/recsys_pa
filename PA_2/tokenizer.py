import re

def tokenize(target_string):
	#word_list = re.findall(r"[\w']+", target_string)
	word_list = re.findall(r"[\w]+\'[\w]+|[\w]+\-[\w]+|[\w]+", target_string)
	return word_list

def nltk_english_stop_words():
	return {'those', 'not', 'you', 'having', 'will', 'to', 't', "you'll", "didn't", 'her', 'no', 'can', 'yourselves', 'doing', 'just', 'down', 'all', 'yourself', 'nor', 'wasn', 'for', 'before', 'had', 'did', 'd', 'now', 'does', 'll', 'm', "mightn't", 'this', 'them', 'a', 'won', 'about', 'that', 'wouldn', "don't", 'shouldn', 'an', "needn't", 'hers', 'at', 'your', 'each', 'who', 'where', 'itself', 'so', 'ma', 'when', 'below', "it's", 'do', 'in', 'mustn', 'their', 'should', 'because', 'other', 'only', 'they', 'he', 'further', 'couldn', 'there', 'my', 'of', 'while', 'am', 'and', 'or', 'any', 'with', 'isn', "mustn't", 'theirs', 'herself', 'were', 'me', "she's", 'it', 'been', 'i', "you've", 'until', 'very', 'being', 'himself', 'we', 'out', 'needn', 'was', 'weren', 'are', 'these', 'once', "couldn't", 'didn', "haven't", 'hadn', 'aren', 'between', 'if', 'here', 'why', "isn't", 'during', 'over', 'same', 'more', 'be', 'than', "you'd", 'myself', 'above', 'own', "hadn't", 'hasn', "wouldn't", 'such', 'what', 're', 'mightn', 'is', 'have', 'y', 'off', 'under', 'o', 'she', 'into', 'yours', 'shan', 'on', 'as', 'most', 'has', "doesn't", 'him', 'doesn', 's', 'then', 'how', 'ain', "shan't", "wasn't", 'through', "won't", 'its', 'from', 'by', "shouldn't", 'after', 'both', 'the', "should've", "hasn't", 'up', 'ours', "you're", 'don', 'haven', 'but', 'themselves', 'which', 'few', "that'll", 'his', 'our', 've', "weren't", 'too', "aren't", 'some', 'again', 'whom', 'ourselves', 'against'}

def not_stop_words(tokens):
	return [token for token in tokens if token not in nltk_english_stop_words()]
if __name__ == '__main__':
	
	target_string = "My name's maximums, my un-luck numbers are 12 45 78. Who - he  asked?"
	# split on white-space 
	#word_list = re.split(r"\s+", target_string)
	print(tokenize(target_string))
	print(not_stop_words(tokenize(target_string)))
	
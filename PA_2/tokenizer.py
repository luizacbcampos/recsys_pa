import re
from num2word import num2words
from snowball_stemmer import Stemmer

def tokenize(target_string):
	'''
		Tokenizes a string
	'''
	#word_list = re.findall(r"[\w']+", target_string)
	word_list = re.findall(r"[\w]+\'[\w]+|[\w]+\-[\w]+|[\w]+", target_string)
	return word_list

def tokenization(target_string, lower_=True, number=True):
	'''
		String tokenization
		lower_: lowers string
		number: converts number to text
		apostrophe: removes apostrophe
	'''
	if lower_:
		target_string = target_string.lower()		

	if number:
		cardinal_pattern = r'([\d]+\.[\d]|[\d]+)(?![\w])'
		ordinal_pattern = r'([\d]*1[ ]*st|[\d]*2[ ]*nd|[\d]*3[ ]*rd|[\d]*3[ ]*rd|[\d]+[ ]*th)(?![\w])'
		#target_string = re.sub(r'[\d]+', lambda m: num2words(m.group(), to='cardinal'), target_string)
		target_string = re.sub(cardinal_pattern, lambda m: num2words(m.group(), to='cardinal'), target_string)
		target_string = re.sub(ordinal_pattern, lambda m: num2words(re.match(r'[\d]+',m.group()).group(), ordinal=True, to='ordinal'), target_string)

	word_list = tokenize(target_string)
	return word_list

def nltk_english_stop_words():
	return {'those', 'not', 'you', 'having', 'will', 'to', 't', "you'll", "didn't", 'her', 'no', 'can', 'yourselves', 'doing', 'just', 'down', 'all', 'yourself', 'nor', 'wasn', 'for', 'before', 'had', 'did', 'd', 'now', 'does', 'll', 'm', "mightn't", 'this', 'them', 'a', 'won', 'about', 'that', 'wouldn', "don't", 'shouldn', 'an', "needn't", 'hers', 'at', 'your', 'each', 'who', 'where', 'itself', 'so', 'ma', 'when', 'below', "it's", 'do', 'in', 'mustn', 'their', 'should', 'because', 'other', 'only', 'they', 'he', 'further', 'couldn', 'there', 'my', 'of', 'while', 'am', 'and', 'or', 'any', 'with', 'isn', "mustn't", 'theirs', 'herself', 'were', 'me', "she's", 'it', 'been', 'i', "you've", 'until', 'very', 'being', 'himself', 'we', 'out', 'needn', 'was', 'weren', 'are', 'these', 'once', "couldn't", 'didn', "haven't", 'hadn', 'aren', 'between', 'if', 'here', 'why', "isn't", 'during', 'over', 'same', 'more', 'be', 'than', "you'd", 'myself', 'above', 'own', "hadn't", 'hasn', "wouldn't", 'such', 'what', 're', 'mightn', 'is', 'have', 'y', 'off', 'under', 'o', 'she', 'into', 'yours', 'shan', 'on', 'as', 'most', 'has', "doesn't", 'him', 'doesn', 's', 'then', 'how', 'ain', "shan't", "wasn't", 'through', "won't", 'its', 'from', 'by', "shouldn't", 'after', 'both', 'the', "should've", "hasn't", 'up', 'ours', "you're", 'don', 'haven', 'but', 'themselves', 'which', 'few', "that'll", 'his', 'our', 've', "weren't", 'too', "aren't", 'some', 'again', 'whom', 'ourselves', 'against'}

def not_stop_words(tokens):
	'''
		Returns a list of NON-STOP words
	'''
	return [token for token in tokens if token not in nltk_english_stop_words()]

def remove_punctuation(word_list):
	'''
		Removes punctuation from string list
	'''
	punct = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'
	for i in range(len(word_list)):
		word_list[i] = word_list[i].translate(str.maketrans('', '', punct))

	return word_list

def remove_apostrophe(tokens):
	'''
		Removes apostrophe
	'''
	for i in range(len(tokens)):
		tokens[i] = tokens[i].replace("'", "")
	return tokens

def tokenize_plot(plot, lower_=True, number=True, apostrophe=True, punctuation=True, stemmer=None):
	'''
		Returns the plot tokenized in list format
	'''
	word_list = tokenization(plot, lower_, number)
	
	if punctuation:
		word_list = remove_punctuation(word_list)
	
	tokens = not_stop_words(word_list)	
	
	if apostrophe:
		tokens = remove_apostrophe(tokens)

	if stemmer != None:
		tokens = stemmer.stemWords(tokens)
		tokens = not_stop_words(tokens) #might create stop words
	
	return tokens

def set_tokenize_plot(plot, lower_=True, number=True, apostrophe=True, punctuation=True, stemmer=None):
	'''
		Returns the plot tokenized in set format
	'''
	word_list = set(tokenization(plot, lower_, number))

	if punctuation:
		word_list = remove_punctuation(word_list)

	tokens = not_stop_words(word_list)

	if apostrophe:
		tokens = remove_apostrophe(tokens)

	if stemmer != None:
		tokens = stemmer.stemWords(tokens)
		tokens = not_stop_words(tokens) #might create stop words

	return set(tokens)


def create_word_set(json_dicio, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball'):
	'''
		Creates a set with every word on the plots
	'''
	wordSet = set()
	for dicio in json_dicio:
		tokens = set_tokenize_plot(dicio['Plot'], lower_, number, apostrophe, punctuation)
		wordSet = wordSet.union(tokens)
	return wordSet

def create_word_set_and_dict(json_dicio, lower_=True, number=True, apostrophe=True, punctuation=True, stem='snowball'):
	'''
		Creates a set with every word on the plots. Creates a dict with each ItemId's tokens
	'''
	wordSet = set()
	token_dict = {}

	if stem == 'snowball':
		stemmer = Stemmer('english')
	else:
		stemmer = None

	for dicio in json_dicio:
		tokens = tokenize_plot(dicio['Plot'], lower_, number, apostrophe, punctuation, stemmer)
		wordSet = wordSet.union(set(tokens))
		token_dict[dicio['ItemId']] = tokens
	
	return wordSet, token_dict

def make_wordSetDict(wordSet):
	'''
		Creates a count dict
	'''
	return dict.fromkeys(wordSet, 0)

def make_ItemId_wordDict(wordSet, tokens):
	'''
		Counts ocurrence of word in tokens
	'''
	wordDict = make_wordSetDict(wordSet)
	for word in tokens:
		wordDict[word]+=1
	return wordDict


def computeTF(wordSet, tokens):
    tfDict = {}
    tokensCount = len(tokens)
    wordDict = make_ItemId_wordDict(wordSet, tokens)
    for word, count in wordDict.items():
        tfDict[word] = count/float(tokensCount)
    return tfDict


def computeIDF(wordSet, token_dict):
 
    N = len(token_dict)
    idfDict = make_wordSetDict(wordSet)

    for itemId, tokens in token_dict.items():
    	for word in set(tokens):
    		idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = np.log10(N / float(val))
        
    return idfDict


if __name__ == '__main__':
	
	target_string = "My name's maximums, my un-luck numbers are 12 45th 7.8. Who - he  asked?"
	# split on white-space 
	#word_list = re.split(r"\s+", target_string)
	print(tokenize(target_string))
	print(not_stop_words(tokenize(target_string)))
	

	math='<m>3+5</m>'
	print(re.sub(r'<(.)>(\d+?)\+(\d+?)</\1>', lambda m: str(int(m.group(2)) + int(m.group(3))), math))

	print(re.sub(r'[\d]+', lambda m: num2words(m.group(), to='cardinal'), target_string))
	print(re.sub(r'([\d]+\.[\d]|[\d]+)(?![\w])', lambda m: num2words(m.group(), to='cardinal'), target_string))
	print(re.sub(r'([\d]*1[ ]*st|[\d]*2[ ]*nd|[\d]*3[ ]*rd|[\d]*3[ ]*rd|[\d]+[ ]*th)(?![\w])', lambda m: num2words(re.match(r'[\d]+',m.group()).group(), ordinal=True, to='ordinal'), target_string))

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np


def remove_stopwords(documents):
	'''
		fn: Removes the Stop words from all the documents.sidebar
		
		input: list of documents
		return: list of documnents after removing stopwords
	'''
	new_docs = []
	for doc in documents:
		word_list = word_tokenize(doc)
		filtered_words = [word for word in word_list if word not in stopwords.words('english')]
		document = " ".join(filtered_words)
		new_docs.append(document)

	return new_docs

def get_maxlen_on_percentile(documents, percentile):
	'''
		fn: Get Maxlen of Token's based on Percentile
		
		input: list of documents, percentile for cut off
		return: number of tokens based on percentile
	'''
	len_docs = []
	for doc in documents:
		word_list = word_tokenize(doc)
		len_words = len(word_list)
		len_docs.append(len_words)
	np_array = np.array(len_docs)
	max_len = int(np.percentile(np_array, percentile))

	return max_len

def get_list_of_list_docs(documents):
	'''
		fn: Get list of list for Input to Gensim for w2v model
		
		input: list of documents
		return: list of list of documents with word_tokens
	'''
	docs = []
	for doc in documents:
		word_list = word_tokenize(doc)
		docs.append(word_list)

	return docs

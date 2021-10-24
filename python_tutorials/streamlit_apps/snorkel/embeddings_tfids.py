from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd


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

def get_sklearn_tfidf_vectors(document_list):
	document_list = remove_stopwords(documents=document_list)
	vectorizer = TfidfVectorizer()
	vectors = vectorizer.fit_transform(document_list)
	feature_names = vectorizer.get_feature_names()
	dense = vectors.todense()
	denselist = dense.tolist()
	df = pd.DataFrame(denselist, columns=feature_names)

	return df

def get_sklearn_count_vectors(document_list):
	document_list = remove_stopwords(documents=document_list)
	vectorizer = CountVectorizer()
	vectors = vectorizer.fit_transform(document_list)
	feature_names = vectorizer.get_feature_names()
	cnt_arrays = vectors.toarray()
	df = pd.DataFrame(cnt_arrays, columns=feature_names)

	return df






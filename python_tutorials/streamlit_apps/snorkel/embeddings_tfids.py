from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
from utils import remove_stopwords


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






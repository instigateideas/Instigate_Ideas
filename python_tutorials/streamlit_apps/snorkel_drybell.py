import streamlit as st
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

st.title("Snorkel Drybell Architecture")

st.write(
'''
	The Snorkel Drybell is an architecture devloped by google. It consists of three important layers

	* Weak Classifiers Layers
	* Discriminative Layer
	* Soft Voting Layer (Ensemble Technique)

	It is a kind of structure which help us in identifying more hams from the text data where robust
	model is needed. 
'''
)

text_datasets = ("imdb_dataset","fetch_20newsgroups")
weak_classifiers = ('Logistic Regression', 'Decision Tree', 'Random Forest', \
					'SVC', 'Naive Bayes', 'GBM', 'XGBoost')


dataset_name = st.sidebar.selectbox("Select the Text dataset", text_datasets)
header_text = st.sidebar.header("Weak Classifier Layer")

def load_data(data_path, ext='csv'):
	if ext == 'csv':
		data = pd.read_csv(data_path)
	else:
		raise TypeError(f"File Format '{ext}' is Unreadable")

	return data

@st.cache
def get_dataset(dataset_name):
	if dataset_name == "fetch_20newsgroups":
		data = datasets.fetch_20newsgroups(subset='all')
		X = data.data
		y = data.target
	elif dataset_name == "imdb_dataset":
		data = load_data("./data/imdb_dataset.csv")
		X = data["review"]
		y = data["sentiment"]
	else:
		data = datasets.load_wine()

	return X, y, data

data_load_state = st.text("Load data...")
X, Y, data = get_dataset(dataset_name)
data_load_state.text("Loading data... done!")

# Showing data
st.subheader("Raw data")
st.write(data.head())

# Select the Weak Classifiers
selected_values = st.sidebar.multiselect("Select Weak Classifiers", weak_classifiers)

# st.sidebar.write(selected_values)


def check_model_exist(model_name):
	if model_name in weak_classifiers:
		return True
	else:
		return False

def add_params_to_dict(params, clf_sel, **kwargs):
	if clf_sel not in params:
		params[clf_sel] = {}
		params[clf_sel].update(**kwargs)
	else:
		params[clf_sel].update(**kwargs)

	return params

## TODO: Fix the dictinonary to get all the params
def get_clf_parameters(selected_values):
	params = dict()
	for clf_sel in selected_values:
		st.sidebar.header(f"{clf_sel} Parameters")
		if check_model_exist(model_name=clf_sel):
			if clf_sel == "Logistic Regression":
				max_iter = st.sidebar.slider("max_iter", 100, 300)
				random_state = st.sidebar.text_input("random_state", 32)
				param_log = {"max_iter": max_iter, "random_state": random_state}
				params.update(add_params_to_dict(params=params, clf_sel=clf_sel, param=param_log))
			elif clf_sel == "Decision Tree":
				st.sidebar.write("Decision Tree params goes here..")
			elif clf_sel == "Random Forest":
				n_estimators = st.sidebar.slider("n_estimators", 10, 100)
				criterion = st.sidebar.selectbox('criterion',('gini', 'entropy'))
				param_rf = {"n_estimators": n_estimators, "criterion": criterion}
				params.update(add_params_to_dict(params=params, clf_sel=clf_sel, param=param_rf))
			elif clf_sel == "SVC":
				st.sidebar.write("Logistic reg params goes here..")
			elif clf_sel == "GBM":
				st.sidebar.write("Logistic reg params goes here..")
			elif clf_sel == "XGBoost":
				st.sidebar.write("Logistic reg params goes here..")

	return params


params = get_clf_parameters(selected_values)
st.write(params)
st.sidebar.button("Submit")

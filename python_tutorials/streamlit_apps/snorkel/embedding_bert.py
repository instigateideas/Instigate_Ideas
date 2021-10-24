# import torch
from transformers import BertTokenizer, BertModel

test_text = """
India, officially the Republic of India (Hindi: Bhārat Gaṇarājya) is a country in South Asia. It is the seventh-largest country by area, the second-most populous country, and the most populous democracy in the world. Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west.
"""

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def get_marked_text(text_data):
	marked_text = "[CLS]" + text_data.replace(".", ". [SEP]")

	return marked_text


def tokenize_document(text_data):
	marked_text = get_marked_text(text_data)
	tokenized_text = tokenizer.tokenize(marked_text)

	return tokenized_text

def convert_token_to_ids(tokenized_text):
	indexed_text = tokenizer.convert_tokens_to_ids(tokenized_text)

	return indexed_text

def view_tokenized_text_with_ids(token_text, index_text):
	# Display the words with their indeces.
	for tup in zip(token_text, index_text):
		print('{:<12} {:>6,}'.format(tup[0], tup[1]))

token_text = tokenize_document(text_data=test_text)
index_text = convert_token_to_ids(tokenized_text=token_text)

view_tokenized_text_with_ids(token_text=token_text, index_text=index_text)



def get_bert_embeddings(sentences):
	result = bert_obj(sentences)

	return result

def flat_tokens_embeddings(result):
	t = []
	e = []
	for i in result:
		t.append(i[0])
		e.append(i[1])
	text_flat = [item for sublist in t for item in sublist]
	emb_flat = [item for sublist in e for item in sublist]
	a = [text_flat,emb_flat]

	return a

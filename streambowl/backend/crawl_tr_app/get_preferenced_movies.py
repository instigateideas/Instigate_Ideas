from insert_parsed_to_db import *
from flask import Flask, request
from flask import json

app = Flask(__name__)

preferred_quality = [1, 2]
prefered_language = "Tamil"
movie_db_collection_name = "movies_data_collection" 

@app.route('/prefered/movies_list', methods=['GET', 'POST'])
def get_movie_list():
	data = request.get_data()
	print(data)
	print(type(data))
	pg_no = json.loads(data)
	print(pg_no)
	resp_data = apply_language_and_quality_filter(collection_name=movie_db_collection_name, \
							prefered_quality_list=preferred_quality, \
							prefered_language=prefered_language, page=pg_no["page_no"])
	print(resp_data)

	response = app.response_class(
	status=200,
	response=json.dumps(resp_data),
	mimetype='application/json'
		)

	return response

@app.route("/prefered/movies_count", methods=['GET', 'POST'])
def movie_count():
	resp_count = get_prefered_movie_count(collection_name=movie_db_collection_name, \
							prefered_quality=preferred_quality, \
							prefered_language=prefered_language)
	response = app.response_class(
	status=200,
	response=json.dumps(resp_count),
	mimetype='application/json'
		)

	return response

@app.route('/health_check', methods=['GET'])
def health_status():

	data = {"status": "server is live"}

	resp = app.response_class(
	status=200,
	response=json.dumps(data),
	mimetype='application/json'
		)
	
	return resp

if __name__ == "__main__":
	app.run(debug=True, port=5001, host="0.0.0.0",)













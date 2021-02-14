from bs4 import BeautifulSoup
import pymongo
import math
import re

database_name = "movie_database"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
preferred_quality = [1, 2]
prefered_language = "Tamil"

def insert_to_mongodb(data, collection_name):
	mydb = myclient[database_name]
	mycol = mydb[collection_name]
	for datum in data:
		try:
			mycol.insert_one(datum)
		except pymongo.errors.DuplicateKeyError:
			continue

	get_count_of_collection(collection_name=collection_name)

def insert_document_to_mongodb(datum, collection_name):
	mydb = myclient[database_name]
	mycol = mydb[collection_name]
	try:
		mycol.insert_one(datum)
	except pymongo.errors.DuplicateKeyError:
		pass

def get_list_of_collection_names():
	db = myclient[database_name]

	return db.collection_names()

def drop_collection(collection_name):
	db = myclient[database_name]

	db[collection_name].drop()
	print("The Collection - {} deleted from Database {}".format(collection_name, database_name))

def mongo_server_status():
	db = myclient[database_name]
	status = db.command("serverStatus")
	print("The the staus of the server: {}".format(status))
	
	return status

def mongo_db_status():
	db = myclient[database_name]
	status = db.command("dbstats")
	print("The the staus of the database: {}".format(status))
	
	return status

def search_a_movie(movie_name, collection_name):
	db = myclient[database_name]
	results = db[collection_name].find({"movie_title": {'$regex': movie_name, '$options': 'i'}})

	return results

def get_count_of_collection(collection_name):
	db = myclient[database_name]
	n_movies = db[collection_name].find().count()

	print("The Number of Documents in the {} is {}".format(collection_name, n_movies))

	return n_movies

def filter_based_on_quality_pref(collection_name, prefered_quality_list):
	db = myclient[database_name]
	quality_preferred =max(prefered_quality_list)
	# get higher qulaity score starts from 1 - 6
	quality_movies = db[collection_name].find({"movie_score": {'$lt': quality_movies}})

	return quality_movies

def get_currently_scraped_data_from_db(collection_name, epoch):
	db = myclient[database_name]
	docs = db[collection_name].find({"current_timestamp": {"$gt": epoch}})
	print(docs)
	movies = []
	for doc in docs:
		movies.append(doc)

	return movies

def no_of_pages_based_on_limit(total_count, limit=5):
	no_data = total_count["total_movie_count"]
	pages =math.ceil(no_data/limit)
	total_count["no_of_pages"] = pages
	return total_count

def get_prefered_movie_count(collection_name, prefered_quality, prefered_language):
	db = myclient[database_name]
	quality_preferred =max(prefered_quality)+1
	aggr = [{'$unwind': '$audio_languages'}, \
			{'$match': {"audio_languages": { '$regex': prefered_language, '$options': 'i' }}}, \
			{'$match': {"movie_score": {'$lt': quality_preferred}}},\
			{'$match': {"magnet_link_flag": True }}, \
			{ "$group" : {
			"_id" : {"movie_name": "$movie_title", "release_year": "$release_year"},
			"download_links": { "$push" : "$$ROOT" }
				}
			}
			]
	count_of_movies = db[collection_name].aggregate(aggr)
	#print(count_of_movies.count())
	count_of_movies = {"total_movie_count": len(list(count_of_movies))}
	no_of_movies = no_of_pages_based_on_limit(total_count=count_of_movies)

	return no_of_movies


def apply_language_and_quality_filter(collection_name, prefered_quality_list, prefered_language, page=1, limit=5):
	db = myclient[database_name]
	last_page = False
	quality_preferred =max(prefered_quality_list)+1
	if page == 1:
		# First Page
		aggr = [{'$unwind': '$audio_languages'}, \
				{'$match': {"audio_languages": { '$regex': prefered_language, '$options': 'i' }}}, \
				{'$match': {"movie_score": {'$lt': quality_preferred}}},\
				{'$match': {"magnet_link_flag": True }}, \
				{'$sort': {'movie_score': 1}}, \
				{ "$group" : {
							"_id" : {"movie_name": "$movie_title", "release_year": "$release_year"},
							"download_links": { "$push" : "$$ROOT" }
							}
				}, \
				{'$sort': {'_id.release_year': -1}}, \
				{'$limit': limit}
				]
	else:
		# Above Second Page
		skip_no = limit*(page-1)
		aggr = [{'$unwind': '$audio_languages'}, \
				{'$match': {"audio_languages": { '$regex': prefered_language, '$options': 'i' }}}, \
				{'$match': {"movie_score": {'$lt': quality_preferred}}},\
				{'$match': {"magnet_link_flag": True }}, \
				{'$sort': {'movie_score': 1}}, \
				{ "$group" : {
							"_id" : {"movie_name": "$movie_title", "release_year": "$release_year"},
							"download_links": { "$push" : "$$ROOT" }
							}
				}, \
				{'$sort': {'_id.release_year': -1}}, \
				{'$skip': skip_no}, \
				{'$limit': limit}
				]

	movie_data = {"data": []}
	docs = db[collection_name].aggregate(aggr)
	cnt = 0
	for doc in docs:
		movie_data["data"].append(doc)
		cnt+=1
	if cnt < limit:
		last_page = True
	meta = {"returned_count": cnt, "last_page": last_page, "page_no": page, \
	"preferred_language": prefered_language, "preferred_quality": prefered_quality_list}
	movie_data["metadata"] = meta

	return movie_data 

if __name__ == "__main__":
	get_count_of_collection(collection_name="latest_movie_collection")
	apply_language_and_quality_filter(collection_name="latest_movie_collection", \
									prefered_quality_list=preferred_quality, \
									prefered_language=prefered_language, page=2)
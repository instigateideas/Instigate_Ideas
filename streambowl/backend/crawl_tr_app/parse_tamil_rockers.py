from __future__ import division, unicode_literals 
import codecs
from bs4 import BeautifulSoup
from torrent_downloader import start_download
from datetime import datetime
from insert_parsed_to_db import *
import pandas as pd
import json
import requests
import re

tamilrockers_website = "https://tamilrockers.ws/"
tr_webpage = "/home/arunachalam/Documents/output_streambowl/tamilrockers_indexpage.html"
scrapper_host = "http://localhost:5000/get_html_content"
save_location_html = "/home/arunachalam/Documents/output_streambowl"
movie_download_location = "/home/arunachalam/Documents/output_streambowl/movies"

video_codec_index = {"Bluray":1, "HD HEVC": 1, "HD AVC": 1, "HD": 1, "BD": 1, "BR": 1, \
"BDRip": 2, "HDRip": 2, "BRrip": 2, "HDTV": 2, "HDTVRip": 2, "DIVx": 3, "DVD":3, "DVDRip": 3, \
"TVRip": 3, "WEB": 3, "": 0}

video_quality_index = {"1080p": 1, "720p": 2, "480p": 3, "360p": 4, "240p": 5, "": 0}

movie_quality_indicator = {"11": "Awesome Quality", "10": "Awesome Quality", \
							"12": "Best Quality", "01": "Best Quality", "21": "Best Quality", \
							"22" : "Good Quality", "13": "Good Quality", "31": "Good Quality", \
							"20": "Good Quality", "02": "Good Quality", "23": "Less Quality", \
							"32": "Less Quality", "30": "Less Quality", "03": "Less Quality", \
							"14": "Less Quality", "24": "Less Quality", "15": "Less Quality", \
							"04": "Less Quality", "40": "Less Quality", "34": "Niche Quality", \
							"25": "Niche Quality", "35": "Niche Quality", "05": "Niche Quality", \
							"33": "Niche Quality", "50": "Niche Quality", "00": "No Quality Score"}

quality_hierarchy = {"Awesome Quality": 1, "Best Quality": 2, "Good Quality": 3, \
						"Less Quality": 4, "Niche Quality": 5, "No Quality Score": 6}


def extract_from_tamilrockers(web_address):
	scrape_url = {"url": web_address}
	html_response = requests.post(url=scrapper_host, data=json.dumps(scrape_url))
	save_html_file(save_name=tr_webpage, response=html_response)

def extract_first_page_info(file_name):
	data = [] 
	f = codecs.open(file_name, 'r', 'utf-8')
	soup = BeautifulSoup(f.read(), 'html.parser')
	# Remove the overlay that is covering the contents
	soup.find("div", {"id": "overlay"}).decompose()
	# select the element which contains all the movie information
	entire_contents = soup.find("div", {"class": "ipsType_textblock ipsPad"})
	# select the movies element by paragraph
	all_elements = entire_contents.findAll("p", {"style": "text-align:center"})
	print("All elements: ", len(all_elements))
	for ele in all_elements:
		all_url_tags = ele.findAll("a", {"class": "bbc_url"})
		for a_tag in all_url_tags:
			try:
				trid = a_tag['href'].split("showtopic=")[1]
				movie_link = a_tag['href']
				crawled_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
				ts = int(datetime.now().timestamp())
				data.append({"_id": trid, "TRID": trid, "movie_link": movie_link, \
					"crawled_time": crawled_time, "current_timestamp": ts})
				print("TRID: ", trid)
				print("URL: ", movie_link)
				print("\n")
			except IndexError:
				pass
	temp_df = pd.DataFrame(data)
	# Remove Duplicates
	temp_df.drop_duplicates(subset="TRID", keep="first", inplace=True)
	temp_df.reset_index(drop=True, inplace=True)

	return temp_df.to_dict('records')

def save_html_file(save_name, response):
	with open(save_name, "w") as Infile:
		Infile.write(response.text)

def load_soup_of_html_file(html_file):
	with open(html_file, "r") as outfile:
		data = outfile.read()
	soup = BeautifulSoup(data, 'html.parser')
	# Remove the overlay in the HTML saved
	try:
		soup.find("div", {"id": "overlay"}).decompose()
	except AttributeError:
		pass

	return soup

def extract_movie_torrent_information(movie_data, collection_name):
	print("Number of movie data to be scraped: ", len(movie_data))
	cnt = 1
	for movie_datum in movie_data:
		scrape_url = {"url": movie_datum["movie_link"]}
		print("Scrapping... {}".format(scrape_url["url"]))
		html_response = requests.post(url=scrapper_host, data=json.dumps(scrape_url))
		saved_path = f"{save_location_html}/{movie_datum['TRID']}.html"
		save_html_file(save_name=saved_path, response=html_response)
		movie_datum["saved_path"] = saved_path
		print("Extracted torrent info from {} successfully, which is {} out of {}".format(scrape_url["url"], \
			cnt, len(movie_data)))
		cnt+= 1
		insert_document_to_mongodb(datum=movie_datum, collection_name=collection_name)
	get_count_of_collection(collection_name=collection_name)

def get_torrent_magnet_links(html_soup):
	magnet_links = []
	magnet_objects = html_soup.findAll("strong")
	for str_obj in magnet_objects:
		all_img_obj = str_obj.findAll("img", {"class": "bbc_img"})
		for img_obj in all_img_obj:
			if "magnet.png" in img_obj["src"]:
				link_obj = str_obj.find("a", {"title": "External link"})
				magnet_links.append(link_obj["href"])

	return magnet_links


def get_torrent_info(torrent_objs, mag_links):
	torrent_info = []
	cnt = 0
	for torrent_obj in torrent_objs:
		if len(torrent_obj.text) > 0:
			try:
				torrent_data = {"torrent_name": torrent_obj.text, "torrent_url": torrent_obj["href"], "magnet_link": mag_links[cnt]}
			except IndexError:
				# Avoiding if torrent available but no magnetic link errors
				torrent_data = {"torrent_name": torrent_obj.text, "torrent_url": torrent_obj["href"], "magnet_link": ""}
			torrent_info.append(torrent_data)
			cnt+= 1

	return torrent_info

def crt_the_pixel_index(pixel_value):
	pixel_value = int(pixel_value[0:-1])
	if (pixel_value < 1080 and pixel_value > 720):
		return 2
	elif (pixel_value < 720 and pixel_value > 480):
		return 3
	elif (pixel_value < 480 and pixel_value > 360):
		return 4
	elif (pixel_value < 360):
		return 5
	else:
		return 0

def index_mapper_video_codec(datum, value):
	data = video_codec_index
	try:
		datum["video_codec_index"] = data[value]
	except IndexError:
		datum["video_codec_index"] = 0

	return datum

def index_mapper_pixel_quality(datum, value):
	try:
		datum["pixel_quality_index"] = video_quality_index[value]
	except KeyError:
		datum["pixel_quality_index"] = crt_the_pixel_index(pixel_value=value)

	return datum

def size_correct(element):
	try:
		size = element[0]
		return " ".join(size)
	except IndexError:
		return ""

def out_of_list(element):
	try:
		return element[0]
	except IndexError:
		return ""

def validate_flag_elements(soup, tag, element, type):
	flag = False
	if type == "all":
		if soup.find_all(tag, element):
			flag = True
	elif type == "first":
		if soup.find(tag, element):
			flag = True
	else:
		pass

	return flag

def validate_important_fields(soup, datum):
	# important movie title, release year
	imp_fields = [
	{"title_obj": {"tag": "h1", "element": {"class": "ipsType_pagetitle"}, "type": "first"}}, \
	{"image_obj" : {"tag": "img", "element": {"class": "bbc_img"}, "type": "first"}}, \
	{"torrent_obj": {"tag": "a", "element": {"title": "Download attachment"}, "type": "all"}}]
	final_flag = True
	for field in imp_fields:
		selected_element = list(field.keys())[0]
		print(f"Validating the element {selected_element} in DOM for the movie under the url: {datum['movie_link']}")
		status = validate_flag_elements(soup=soup, tag=field[selected_element]["tag"], \
										element=field[selected_element]["element"], \
										type=field[selected_element]["type"])
		print("Status of the Validation: {}".format(status))
		final_flag = final_flag * status

	# Above for loop return 1 or 0 , 1 - incase of validation has passed
	if final_flag == 1:
		datum["validation_flag"] = True
	else:
		datum["validation_flag"] = False

	return final_flag, datum

def parse_movie_data_downloaded(extract_movie_data, collection_name):
	for movie_data in extract_movie_data:
		soup = load_soup_of_html_file(html_file=movie_data["saved_path"])
		validation_flag, movie_data = validate_important_fields(soup=soup, datum=movie_data)
		if validation_flag == 1:
			title_obj = soup.find("h1", {"class": "ipsType_pagetitle"})
			image_obj = soup.find("img", {"class": "bbc_img"})
			torrent_obj = soup.findAll("a", {"title": "Download attachment"})
			movie_info = title_obj.text
			# Movie information extraction with regex
			movie_title = movie_info.split("[")[0]
			movie_title = movie_title.split("(")[0].strip()
			release_year = re.findall(r"\(([0-9]+)\)", movie_info)
			pixel_quality = re.findall(r'[0-9]+p', movie_info)
			video_quality = re.findall(r'(HD HEVC|HD AVC|HDTVRip|HDRip|HDTV|HD|BDRip|BD|BR|WEB|DVDRip|DVD|DIVx|Bluray|TVRip)+', movie_info)
			audio_patterns = re.compile(r'\bKanada\b | \bTelugu\b | \bTamil Dubbed\b | \bHindi\b | \bEng\b | \bTamil\b | \bEnglish\b | \bMalyalam\b', flags=re.I | re.X)
			audio_languages = audio_patterns.findall(movie_info)
			size = re.findall(r'([.0-9]+)+(KB|MB|GB)', movie_info)
			video_codec = re.findall(r'x[0-9]+', movie_info)
			# Adding data to dictionary
			try:
				movie_data["movie_title"] = movie_title
				movie_data["release_year"] = int(out_of_list(element=release_year))
				movie_data["movie_size"] = size_correct(element=size)
				movie_data["movie_poster_link"] = image_obj["src"]
				movie_data["pixel_quality"] = out_of_list(element=pixel_quality)
				movie_data["video_quality"] = out_of_list(element=video_quality)
				movie_data["audio_languages"] = audio_languages
				movie_data["video_codec"] = out_of_list(element=video_codec)
				movie_data = index_mapper_video_codec(datum=movie_data, value=movie_data["video_quality"])
				movie_data = index_mapper_pixel_quality(datum=movie_data, value=movie_data["pixel_quality"])
				movie_code = "{}{}".format(str(movie_data["video_codec_index"]),str(movie_data["pixel_quality_index"]))
				movie_data["movie_grade"] = movie_quality_indicator[movie_code]
				movie_data["movie_score"] = quality_hierarchy[movie_data["movie_grade"]]
				
				# Get the torrent information
				torrent_magnet_links = get_torrent_magnet_links(html_soup=soup)
				if len(torrent_magnet_links) > 0:
					movie_data["magnet_link_flag"] = True
				else:
					movie_data["magnet_link_flag"] = False
				movie_data["torrent_info"] = get_torrent_info(torrent_objs=torrent_obj, \
					mag_links=torrent_magnet_links)
				insert_document_to_mongodb(datum=movie_data, collection_name=collection_name)
			except ValueError:
				# This is to handle the errors that occur in live stream videos,
				# if series video are skipped, if release year is given as an (2008-2020)
				continue
		get_count_of_collection(collection_name=collection_name)



def download_movie(torrent_magnet_link, save_location):
	start_download(save_path=save_location, magnet_link=torrent_magnet_link)

if __name__ == "__main__":
	current_epoch = int(datetime.now().timestamp())
	extract_from_tamilrockers(web_address=tamilrockers_website)
	movies_info = extract_first_page_info(file_name=tr_webpage)
	insert_to_mongodb(data=movies_info, collection_name="tamil_rockers_movies_collection")
	scrapped_movies_info = get_currently_scraped_data_from_db(collection_name="tamil_rockers_movies_collection", epoch=current_epoch)
	extract_movie_torrent_information(movie_data=scrapped_movies_info, collection_name="tamil_rockers_torrent_informations")
	movies_torrent_info = get_currently_scraped_data_from_db(collection_name="tamil_rockers_torrent_informations", epoch=current_epoch)
	parse_movie_data_downloaded(extract_movie_data=movies_torrent_info, collection_name="movies_data_collection")


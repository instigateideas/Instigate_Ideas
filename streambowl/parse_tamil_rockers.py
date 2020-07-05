from __future__ import division, unicode_literals 
import codecs
from bs4 import BeautifulSoup
import json
import requests
import re

file = "file.html"
scrapper_host = "http://localhost:5000/get_html_content"
save_location_html = "/home/arunachalam/Documents/Instigate_Ideas/streambowl/outputs"

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
			# print(a_tag)
			# if len(a_tag.text) > 0:
			# 	if len(a_tag.text.split("[")[0]) > 0:
			try:
				trid = a_tag['href'].split("showtopic=")[1]
				movie_link = a_tag['href']
				data.append({"TRID": trid, "movie_link": movie_link})
				print("TRID: ", trid)
				print("URL: ", movie_link)
				print("\n")
			except IndexError:
				pass

	return data

def save_html_file(save_name, response):
	with open(save_name, "w") as Infile:
		Infile.write(response.text)

def load_soup_of_html_file(html_file):
	with open(html_file, "r") as outfile:
		data = outfile.read()
	soup = BeautifulSoup(data, 'html.parser')
	# Remove the overlay in the HTML saved
	soup.find("div", {"id": "overlay"}).decompose()

	return soup


def extract_movie_information(movie_data):
	new_dict = []
	print("Number of movie data to be scraped: ", len(movie_data))
	for movie_datum in movie_data[0:4]:
		scrape_url = {"url": movie_datum["movie_link"]}
		html_response = requests.post(url=scrapper_host, data=json.dumps(scrape_url))
		saved_path = f"{save_location_html}/{movie_datum['TRID']}.html"
		print(html_response)
		save_html_file(save_name=saved_path, response=html_response)
		movie_datum["saved_path"] = saved_path
		new_dict.append(movie_datum)

	return new_dict

def get_torrent_info(torrent_objs):
	torrent_info = []
	for torrent_obj in torrent_objs:
		if len(torrent_obj.text) > 0:
			torrent_data = {"torrent_name": torrent_obj.text, "torrent_url": torrent_obj["href"]}
			torrent_info.append(torrent_data)

	return torrent_info

def extract_movie_data_to_download(extract_movie_data):
	movie_infomation = []
	for movie_data in extract_movie_data:
		soup = load_soup_of_html_file(html_file=movie_data["saved_path"])
		title_obj = soup.find("h1", {"class": "ipsType_pagetitle"})
		image_obj = soup.find("img", {"class": "bbc_img"})
		torrent_obj = soup.findAll("a", {"title": "Download attachment"})
		movie_info = title_obj.text
		# Movie information extraction with regex
		movie_title = movie_info.split("[")[0]
		release_year = re.findall(r"\(([0-9]+)\)", movie_info)
		pixel_quality = re.findall(r'[0-9]+p', movie_info)
		video_quality = re.findall(r'(HD HEVC|HD AVC|HDRip|HDTVRip|HDTV|HD|BDRip|BD|BR|WEB|DVDRip|DVD|DIVx|Bluray|TVRip)+', movie_info)
		audio_patterns = re.compile(r'\bKanada\b | \bTelugu\b | \bTamil Dubbed\b | \bHindi\b | \bEng\b | \bTamil\b | \bEnglish\b | \bMalyalam\b', flags=re.I | re.X)
		audio_languages = audio_patterns.findall(movie_info)
		size = re.findall(r'([0-9]+)+(KB|MB|GB)', movie_info)
		video_codec = re.findall(r'x[0-9]+', movie_info)
		# Adding data to dictionary
		movie_data["movie_title"] = movie_title
		movie_data["release_year"] = release_year
		movie_data["pixel_quality"] = pixel_quality
		movie_data["video_quality"] = video_quality
		movie_data["audio_languages"] = audio_languages
		movie_data["video_codec"] = video_codec
		movie_data["image_url"] = image_obj["src"]
		movie_infomation.append(movie_data)
		# Get the torrent information
		movie_data["torrent_info"] = get_torrent_info(torrent_objs=torrent_obj)

	return movie_infomation

if __name__ == "__main__":
	movie_urls = extract_first_page_info(file_name=file)
	extracted_movie_data = extract_movie_information(movie_data=movie_urls)
	downloaded_data = extract_movie_data_to_download(extract_movie_data=extracted_movie_data)
	print("Number of Movie Information Downloaded: ", len(downloaded_data))
	print(downloaded_data)



				# movie_title = a_tag.text.split("[")[0]
				# release_year = re.findall(r"\(([0-9]+)\)", a_tag.text)
		# 		pixel_quality = re.findall(r'[0-9]+p', a_tag.text)
		# 		video_quality = re.findall(r'(HD HEVC|HD AVC|HDRip|HDTVRip|HDTV|HD|BDRip|BD|BR|WEB|DVDRip|DVD|DIVx|Bluray|TVRip)+', a_tag.text)
		# 		audio_patterns = re.compile(r'\bKanada\b | \bTelugu\b | \bTamil Dubbed\b | \bHindi\b | \bEng\b | \bTamil\b | \bEnglish\b | \bMalyalam\b', flags=re.I | re.X)
		# 		audio_languages = audio_patterns.findall(a_tag.text)
		# 		size = re.findall(r'([0-9]+)+(KB|MB|GB)', a_tag.text)
		# 		video_codec = re.findall(r'x[0-9]+', a_tag.text)
		# 		try:
		# 			trid = a_tag['href'].split("showtopic=")[1]
		# 			print("TRID: ", trid)
		# 			print("Movie Title: ", movie_title)
		# 			print("Movie Languages: ", audio_languages)
		# 			print("Release Year: ", release_year)
		# 			print("Pixel Quality: ", pixel_quality)
		# 			print("Video Quality: ", video_quality)
		# 			print("Video Codec: ", video_codec)
		# 			print("Size: ", size)
		# 			print("Short Desc: ", a_tag.text)
		# 			print("URL: ", a_tag['href'])
		# 		except IndexError:
		# 			pass
				


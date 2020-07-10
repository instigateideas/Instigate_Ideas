from __future__ import division, unicode_literals 
import codecs
from bs4 import BeautifulSoup
from torrent_downloader import start_download
import pandas as pd
import json
import requests
import re

tamilrockers_website = "https://tamilrockers.ws/"
tr_webpage = "/home/arunachalam/Documents/output_streambowl/tamilrockers_indexpage.html"
scrapper_host = "http://localhost:5000/get_html_content"
save_location_html = "/home/arunachalam/Documents/output_streambowl"
movie_download_location = "/home/arunachalam/Documents/output_streambowl/movies"

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
				data.append({"TRID": trid, "movie_link": movie_link})
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
			torrent_data = {"torrent_name": torrent_obj.text, "torrent_url": torrent_obj["href"], "magnet_link": mag_links[cnt]}
			torrent_info.append(torrent_data)
			cnt+= 1

	return torrent_info

def extract_movie_data_to_download(extract_movie_data):
	movie_infomation = []
	for movie_data in extract_movie_data:
		print(movie_data)
		soup = load_soup_of_html_file(html_file=movie_data["saved_path"])
		title_obj = soup.find("h1", {"class": "ipsType_pagetitle"})
		image_obj = soup.find("img", {"class": "bbc_img"})
		torrent_obj = soup.findAll("a", {"title": "Download attachment"})
		torrent_magnet_obj = soup.findAll("a", {"class": "bbc_url","rel": "nofollow external",  "title": "External link"})
		magnet_torrent_obj = soup.findAll("a", {"class": "bbc_url", "title": "External link"})
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
		# Get the torrent information
		torrent_magnet_links = get_torrent_magnet_links(html_soup=soup)
		print("len of torrent objects: ", len(torrent_obj))
		print("no of torrent magnet links: ", len(torrent_magnet_links))
		movie_data["torrent_info"] = get_torrent_info(torrent_objs=torrent_obj, \
			mag_links=torrent_magnet_links)
		movie_infomation.append(movie_data)

	return movie_infomation

def download_movie(torrent_magnet_link, save_location):
	start_download(save_path=save_location, magnet_link=torrent_magnet_links)

if __name__ == "__main__":
	extract_from_tamilrockers(web_address=tamilrockers_website)
	movie_urls = extract_first_page_info(file_name=tr_webpage)
	extracted_movie_data = extract_movie_information(movie_data=movie_urls)
	downloaded_data = extract_movie_data_to_download(extract_movie_data=extracted_movie_data)
	print("Number of Movie Information Downloaded: ", len(downloaded_data))
	print(downloaded_data)
	magnet_links = downloaded_data[0]["torrent_info"][0]["magnet_link"]
	download_movie(torrent_magnet_link=magnet_links, save_location=movie_download_location)


	# print(downloaded_data[0]["torrent_info"][0]["torrent_url"])
	# tor_link = downloaded_data[0]["torrent_info"][0]["torrent_url"]
	# sample_torrent=movie_download_location+'/sample.torrent'
	# print(sample_torrent)
	# download_movie(save_path=movie_download_location, torrent_link=sample_torrent)




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
				


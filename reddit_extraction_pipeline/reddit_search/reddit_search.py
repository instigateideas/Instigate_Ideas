
import json
import os
import time
import sys
import requests
#sys.path.append("../")
from config import Config


class RedditSearch(object):
	def __init__(self, save_path):
		self.save_path = save_path
		self.default_config = Config()
		self.keywords_list = self.default_config.keywords
		self.username = self.default_config.user_name
		self.password = self.default_config.password
		self.access_key = self.default_config.access_key
		self.secret_key = self.default_config.secret_key

	def create_save_path(self, save_path):
		if not os.path.exists(save_path):
			os.makedirs(save_path)

	def get_url(self, call_count, keyword, after_id=None):
		if call_count == 1:
			base_url = f"https://api.reddit.com/subreddits/search?q={keyword}&limit=100&raw_json=1"
		else:
			base_url = f"https://api.reddit.com/subreddits/search?q={keyword}&after={after_id}&limit=100&raw_json=1"

		return base_url
		
	def get_refresh_access_token(self):
		client_auth = requests.auth.HTTPBasicAuth(self.access_key, self.secret_key)
		post_data = {"grant_type": "password", "username": self.username, "password": self.password}
		headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
		response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
		client = requests.session()
		client.headers = headers
		
		return client

	def refresh_access_token(self, start_time):
		if (time.time() - start_time) > 3200:
			print("Refreshing access token")
			client = get_refresh_access_token()
			start_time = time.time()

		return start_time

	def save_as_json(self, data, path, file_name):
		with open(f"{path}/{file_name}", "w") as outfile:
			outfile.write(json.dumps(data))


	def avoiding_rate_limitation(self, start_time, request_count):
		elapsed_time = (time.time() - start_time)
		if request_count >= 30:
			remaining_time_sleep = 60 - elapsed_time
			print(f"Request crossed 30 per minute, so sleeping for {remaining_time_sleep} seconds")
			time.sleep(remaining_time_sleep)
			# Resetting start time and request counts
			start_time = time.time()
			request_count = 2

		return start_time, request_count

	def search_reddit_api(self, keyword, request_count=1, overall_time = time.time(), last_id=None):
		start_time = time.time()
		data_downloaded = 0
		while True:
			if request_count == 1:
				client = self.get_refresh_access_token()
				request_url = self.get_url(call_count=request_count, keyword=keyword)
				reddit_response = client.get(request_url)
				data = json.loads(reddit_response.content)
				len_data = len(data["data"]["children"])
				data_downloaded = data_downloaded + int(len_data)
				new_file_name = "{}_{}_subreddit_file_{}.json".format(keyword, request_count, len_data)
				self.save_as_json(data=data, path=self.save_path, file_name=new_file_name)
				last_id = data["data"]["after"]
				print("Last subreddit id extracted: ", last_id)
			else:
				request_url = self.get_url(call_count=request_count, keyword=keyword, after_id=last_id)
				reddit_response = client.get(request_url)
				try:
					data = json.loads(reddit_response.content)
				except Exception as e:
					print("Got an error due to over loading the Reddit API")
					print("Sleeping for 1 mins..")
					time.sleep(60)
					request_count = self.search_reddit_api(keyword, request_count=request_count, last_id=last_id)
				len_data = len(data["data"]["children"])
				data_downloaded = data_downloaded + int(len_data)
				new_file_name = "{}_{}_subreddit_file_{}.json".format(keyword, request_count, len_data)
				self.save_as_json(data=data, path=self.save_path, file_name=new_file_name)
				last_id = data["data"]["after"]
				start_time, request_count = self.avoiding_rate_limitation(start_time=start_time, request_count=request_count)
				overall_time = self.refresh_access_token(start_time=overall_time)
			if last_id == None:
				print("Completed extraction total subreddits extracted are: ", data_downloaded)
				break
			request_count = request_count + 1

		return request_count, overall_time


	def reddit_search_all_keywords(self):
		self.create_save_path(save_path=self.save_path)
		cnt = 1
		for keyword in self.keywords_list:
			if cnt == 1:
				request_count, overall_time = self.search_reddit_api(keyword=keyword)
			else:
				request_count, overall_time = self.search_reddit_api(keyword=keyword, request_count=request_count, overall_time=overall_time)


if __name__ == "__main__":
	save_path = "/home/arunachalam/Documents/sense2vec_exp/output_api/subreddits"
	reddit_search = RedditSearch(save_path=save_path)
	reddit_search.reddit_search_all_keywords()





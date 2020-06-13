import requests
import os
import time
import json
from base import Base
from config import Config
from ast import literal_eval
from bs4 import BeautifulSoup


class Extract(object):
    """docstring fos Extract"""
    def __init__(self, extract_source):
        self.default_config = Config()
        self.delta = self.default_config.epochs_delta
        self.base_ = Base()
        self.resume_file = self.default_config.resume_file
        self.host_addr = self.default_config.host_address
        self.src_data = extract_source
        self.rate_limit_per_min = 100

    def get_url(self, subreddit, after, before):
        if self.src_data == "submission":
            api_host = "https://api.pushshift.io/reddit/search/submission/?"
        elif self.src_data == "comments":
            api_host = "http://api.pushshift.io/reddit/comment/search?"
        else:
            print("Please enter the submission or comments to start extract data in source_data variable \
                in config")
        url = api_host +"subreddit={}&after={}&before={}&size={}&metadata=true".format(subreddit, after, before, self.default_config.size)
        
        return url

    def get_dates_frmt(self, date):
        x, y, z = date.split("-")
        
        return int(x), int(y), int(z)

    def extract_prep_epochs(self, ext_start_mn, ext_start_yr, ext_start_dt, ext_end_mn, ext_end_yr, ext_end_dt):
        # start_year, start_month = self.base_.where_to_start(year=acc_yr, month=acc_mn, ext_yr=ext_start_yr, ext_mn=ext_start_mn)
        epochs_ = self.base_.get_epochs(delta= self.delta, st_yr=ext_start_yr, st_mn=ext_start_mn, end_dt=ext_end_dt, end_mn=ext_end_mn, end_yr=ext_end_yr, st_date=ext_start_dt)
        chunks = [[epochs_[i], epochs_[i+1]] for i in range(len(epochs_)-1)]
        #print(chunks)
        
        return chunks

    def clear_encode(self, x):
        return literal_eval(x).decode()

    def alb_extract(self, url):
       dat= json.dumps({"url" : url})
       resp = requests.post(url=self.host_addr, data=dat)

       return json.loads(resp.content)

    def make_requests_vpn(self, uri, max_retries = 5):
        def fire_away(uri, call_cost=0):
            dat= json.dumps({"url": f"{uri}"})
            resp = requests.post(url=self.host_addr, data=dat)
            print(resp.status_code == 200)
            assert resp.status_code == 200
            cleantext = BeautifulSoup(resp.content, "lxml").text
            return json.loads(cleantext), call_cost

        current_tries = 1
        call_cost = 1
        while current_tries < max_retries:
            try:
                time.sleep(1)
                response, call_cost = fire_away(uri, call_cost=call_cost)
                return response, call_cost
            except:
                time.sleep(1)
                call_cost = call_cost+ 1
                current_tries += 1

        return fire_away(uri, call_cost=call_cost)


    def make_request(self, uri, max_retries = 5):
        def fire_away(uri):
            response = requests.get(uri)
            print(response.status_code == 200)
            assert response.status_code == 200
            return json.loads(response.content)
        current_tries = 1
        while current_tries < max_retries:
            try:
                time.sleep(1)
                response = fire_away(uri)
                return response
            except:
                time.sleep(1)
                current_tries += 1
        return fire_away(uri)

    def sleeper_function(self, start_time, cost):
        end_time = time.time() - start_time
        if end_time > 60:
            end_time = 60
        if cost >= self.rate_limit_per_min:
            sleep_time = 60-end_time
            time.sleep(sleep_time)
            print("Avoiding Rate limit by sleeping for {}".format(sleep_time))
            cost = 0
            start_time = time.time()

        return cost, start_time

    def extract_reddit_comments(self, subreddit, epochs, f_path, start_time=time.time(),total_cost=0):
        for num_, epoch in enumerate(epochs):
            url = self.get_url(subreddit=subreddit, after=epoch[0], before=epoch[1])
            print(url)
            data = self.alb_extract(url=url)
            call_cost = 1
            totaldata = data["metadata"]["total_results"]
            file_name = f"{subreddit}_time_{epoch[0]}_{epoch[1]}_data_{totaldata}.json"
            f_path_ = f"{f_path}/{self.base_.path_epochs_to_timestamp(ts=epoch[0])}"
            if not os.path.exists(f_path_):
                os.makedirs(f_path_)
            flag = self.base_.condition_check(limit=500, count=totaldata, data=data, name=file_name, path=f_path_)
            if flag == False:
                total_cost= total_cost+call_cost
                epochs_ = self.base_.epochs_splitter(start_epoch=epoch[0], end_epoch=epoch[1])
                self.extract_reddit_comments(subreddit=subreddit, epochs=epochs_, f_path=f_path, start_time=start_time, total_cost=total_cost)
                total_cost, start_time = self.sleeper_function(start_time=start_time, cost=total_cost)
            total_cost = total_cost+call_cost
            total_cost, start_time = self.sleeper_function(start_time=start_time, cost=total_cost)

        return start_time, total_cost
            

    def start_extraction(self, subreddit, start_date, end_date, base_path, start_time, total_cost):
        ext_start_dt, ext_start_mn, ext_start_yr = self.get_dates_frmt(start_date)
        ext_end_dt, ext_end_mn, ext_end_yr = self.get_dates_frmt(end_date)
        epochs = self.extract_prep_epochs(ext_start_mn=ext_start_mn, ext_start_yr=ext_start_yr, \
            ext_start_dt=ext_start_dt,ext_end_mn=ext_end_mn, ext_end_yr=ext_end_yr, \
            ext_end_dt=ext_end_dt)
        start_time, total_cost = self.extract_reddit_comments(subreddit=subreddit, epochs=epochs, \
            f_path=base_path, start_time=start_time, total_cost=total_cost)
        self.base_.write_resume_file(file_path=self.resume_file, subreddit_completed=subreddit)

        return start_time, total_cost


    def start_extraction_task(self, subreddits, start_date, end_date, base_path):
        ext_start_dt, ext_start_mn, ext_start_yr = self.get_dates_frmt(start_date)
        ext_end_dt, ext_end_mn, ext_end_yr = self.get_dates_frmt(end_date)
        epochs = self.extract_prep_epochs(ext_start_mn=ext_start_mn, ext_start_yr=ext_start_yr, \
            ext_start_dt=ext_start_dt,ext_end_mn=ext_end_mn, ext_end_yr=ext_end_yr, \
            ext_end_dt=ext_end_dt)
        start_time = time.time()
        cost = 0
        for subreddit in subreddits:
            start_time, cost = self.extract_reddit_comments(subreddit=subreddit, epochs=epochs, f_path=base_path, \
             start_time=start_time, total_cost=cost)
            self.base_.write_resume_file(file_path=self.resume_file, subreddit_completed=subreddit)

    def generate_url_for_a_subreddit(self, subreddit, start_date, end_date):
        ext_start_dt, ext_start_mn, ext_start_yr = self.get_dates_frmt(start_date)
        ext_end_dt, ext_end_mn, ext_end_yr = self.get_dates_frmt(end_date)
        epochs = self.extract_prep_epochs(ext_start_mn=ext_start_mn, ext_start_yr=ext_start_yr, \
            ext_start_dt=ext_start_dt,ext_end_mn=ext_end_mn, ext_end_yr=ext_end_yr, \
            ext_end_dt=ext_end_dt)
        urls = []
        for num_, epoch in enumerate(epochs):
            urls.append(self.get_url(subreddit=subreddit, after=epoch[0], before=epoch[1]))

        return urls

    def get_urls_for_all_subreddits(self, subreddits, start_date, end_date):
        all_urls = []
        for subreddit in subreddits:
            all_urls.extend(self.generate_url_for_a_subreddit(subreddit=subreddit, \
                start_date=start_date, end_date=end_date))

        return all_urls

    def extract_data_from_url(self, link):
        subreddit = link.split("subreddit=")[1].split("&")[0]
        epoch_1 = link.split("after=")[1].split("&")[0]
        epoch_2 = link.split("before=")[1].split("&")[0]

        return subreddit, epoch_1, epoch_2

    def url_based_extraction(self, links, base_path):
        start_time=time.time()
        total_cost=0
        for link in links:
            print(link)
            data = self.make_request(uri=link)
            call_cost = 1
            totaldata = data["metadata"]["total_results"]
            subreddit, epoch_1, epoch_2 = self.extract_data_from_url(link=link)
            file_name = f"{subreddit}_time_{epoch_1}_{epoch_2}_data_{totaldata}.json"
            f_path_ = f"{base_path}/{self.base_.path_epochs_to_timestamp(ts=int(epoch_1))}"
            if not os.path.exists(f_path_):
                os.makedirs(f_path_)
            flag = self.base_.condition_check(limit=500, count=totaldata, data=data, name=file_name, path=f_path_)
            if flag == False:
                total_cost= total_cost+call_cost
                total_cost, start_time = self.sleeper_function(start_time=start_time, cost=total_cost)
            self.base_.write_resume_file(file_path=self.resume_file, subreddit_completed=link)







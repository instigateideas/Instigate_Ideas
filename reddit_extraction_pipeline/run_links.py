from config import Config
from base import Base
from extract import Extract
import time

class Run_Reddit_Comment_Extraction(object):
    """docstring fos Run"""
    def __init__(self):
        self.default_config = Config()
        self.st_dt = self.default_config.start_date
        self.end_dt = self.default_config.end_date
        self.sav_path = self.default_config.output_path
        self.resume_file = self.default_config.resume_file

    def run_extraction(self):
        extract_ = Extract()
        base_ = Base()
        list_subreddits_data = base_.get_data_list_subreddits()
        downloaded_subs = base_.check_resume_file(file_path=self.resume_file)
        start_time = time.time()
        cost = 0
        urls = extract_.get_urls_for_all_subreddits(subreddits=list_subreddits_data, \
            start_date=self.st_dt, end_date=self.end_dt)
        if len(downloaded_subs) > 0:
            urls_ = list(set(urls)- set(downloaded_subs))
            print("Already Dowloaded {} sub-reddits yet to download {} sub-reddits".format(len(downloaded_subs), len(urls_)))
            print("Completed {}%".format(len(downloaded_subs)/len(urls_)))
            extract_.url_based_extraction(links=urls_, base_path=self.sav_path)
        else:
            extract_.url_based_extraction(links=urls, base_path=self.sav_path)

if __name__ == "__main__":
    run = Run_Reddit_Comment_Extraction()
    run.run_extraction()

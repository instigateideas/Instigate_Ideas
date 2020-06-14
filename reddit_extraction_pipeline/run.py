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
        if len(downloaded_subs) > 0:
            remianing_list = list(set(list_subreddits_data)- set(downloaded_subs))
            print("Already Dowloaded {} sub-reddits yet to download {} sub-reddits".format(len(downloaded_subs), len(remianing_list)))
            print("Completed {}%".format(len(downloaded_subs)/len(list_subreddits_data)))
            list_subreddits_data = remianing_list
        start_time = time.time()
        cost = 0
        for subreddit in list_subreddits_data:
            start_time, cost = extract_.start_extraction(subreddit=subreddit, start_date=self.st_dt, end_date=self.end_dt, \
                base_path=self.sav_path, start_time=start_time, total_cost=cost)
            print(cost)
            print(start_time)

if __name__ == "__main__":
    run = Run_Reddit_Comment_Extraction()
    run.run_extraction()

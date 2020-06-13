from glob import glob
import json
import os
from tqdm import tqdm
import pandas as pd
from ast import literal_eval
from datetime import datetime, timezone
from config import Config


class  Base(object):
    """docstring for  Base"""
    def __init__(self):
        self.default_config = Config()
        self.subreddit_json_path = self.default_config.subreddit_json_path


    def read_json_file(self, path):
        with open(path, "r") as Infile:
            data = json.loads(Infile.read())
            
        return data

    def save_as_json(self, data, path, file_name):
        with open(f"{path}/{file_name}", "w") as outfile:
            outfile.write(json.dumps(data))

    def get_list_of_subreddits(self, file_path):
        data_ = {"created_date": [],"list_of_subreddits": []}
        list_of_subreddits = []
        print("Getting list of subreddits...")
        for file in tqdm(glob(file_path+"/*.json")):
            data = self.read_json_file(path=file)
            for datum in data["data"]["children"]:
                data_["created_date"].append(datum["data"]["created_utc"])
                data_["list_of_subreddits"].append(datum["data"]["display_name"])
            
        return data_

    def convert_to_timestamp_from_epoch(self, epoch):
        try:
            timestamp = epoch
            if timestamp>0:
                #timedate = datetime.fromtimestamp(timestamp)
                timedate_utc = datetime.fromtimestamp(timestamp, timezone.utc)
            #print ("Time/date: ", format(timedate))
            #print ("Time/date in UTC: ", format(timedate_utc))
        except ValueError:
            print ("Timestamp should be a positive integer, please.")
            
        return timedate_utc

    def path_epochs_to_timestamp(self, ts):
        fmt = "%Y/%m"
        # UTC time
        t = datetime.fromtimestamp(ts, timezone.utc)

        return t.strftime(fmt)

    def get_data_list_subreddits(self):
        temp_df = pd.DataFrame(self.get_list_of_subreddits(file_path=self.subreddit_json_path))
        temp_df["subreddit_created_date"] = temp_df["created_date"].apply(lambda x: self.convert_to_timestamp_from_epoch(x))
        temp_df["year"] = temp_df["created_date"].apply(lambda x: self.convert_to_timestamp_from_epoch(x).year)
        temp_df["month"] = temp_df["created_date"].apply(lambda x: self.convert_to_timestamp_from_epoch(x).month)
        temp_df = temp_df.sort_values(["year", "month"], ascending=False)
        subreddits = list(temp_df["list_of_subreddits"])
        print("Number of Unique sub-reddits: {}".format(len(subreddits)))
    
        return subreddits


    def get_epochs(self, st_yr, st_mn, delta, end_yr, end_mn, end_dt, st_date=1):
        epochs = []
        flag = False
        end_epoch = datetime(end_yr, end_mn, end_dt, 23, 59, 59, tzinfo=timezone.utc).timestamp()
        start_epoch = datetime(st_yr, st_mn, st_date, 0, 0, tzinfo=timezone.utc).timestamp()
        for i in range(int(start_epoch), int(end_epoch)+delta, delta):
            if end_epoch > i:
                epochs.append(i)
            else:
                flag = True
        if flag == True:
            epochs.append(int(end_epoch))
            
        return epochs

    def where_to_start(self, year, month, ext_yr, ext_mn):
        acc_start_epoch = datetime(year, month, 1, 0, 0, tzinfo=timezone.utc).timestamp()
        ext_start_epoch = datetime(ext_yr, ext_mn, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp()
        if acc_start_epoch <= ext_start_epoch:
            year = ext_yr
            month = ext_mn
            
        return year, month

    def epochs_splitter(self, start_epoch, end_epoch):
        mid = (int(start_epoch) + int(end_epoch)) / 2
        mid_start = [int(start_epoch), int(mid)]
        mid_end = [int(mid), int(end_epoch)]
        
        return [mid_start, mid_end]

    def condition_check(self, count, limit, name, data, path):
        if count <= limit:
            if count != 0:
                print("Saving the file..")
                self.save_as_json(data=data, file_name=name ,path=path)
            flag = True
        else:
            print("No data..")
            flag = False
        
        return flag

    def write_resume_file(self, file_path, subreddit_completed):
        with open(file_path, 'a') as outfile:
            outfile.write(subreddit_completed+"\n")

    def check_resume_file(self, file_path):
        if os.path.exists(file_path):
            print("Resuming operations...")
            with open(file_path, "r") as Infile:
                data = Infile.read()
            subreddits = data.split("\n")
        else:
            print("New Extraction Started...")
            subreddits = []

        return subreddits



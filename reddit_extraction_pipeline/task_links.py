from config import Config
from base import Base
from extract import Extract
import luigi


class Reddit_Comment_Task(luigi.Task):
    subreddit_chunk = luigi.FloatParameter()
    sav_path = luigi.Parameter()

    def run(self):
        extract_ = Extract()
        extract_.url_based_extraction(links=subreddit_chunks[self.subreddit_chunk], base_path=self.sav_path)


class Task_getter():
    def __init__(self):
        self.default_config = Config()
        self.st_dt = self.default_config.start_date
        self.end_dt = self.default_config.end_date
        self.sav_path = self.default_config.output_path
        self.resume_file = self.default_config.resume_file
        self.chunk_size = self.default_config.chunk_size

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i: i + n]

    def get_subreddits_links_to_build_task(self):
        base_ = Base()
        extract_ = Extract()
        list_subreddits_data = base_.get_data_list_subreddits()
        downloaded_subs = base_.check_resume_file(file_path=self.resume_file)
        urls = extract_.get_urls_for_all_subreddits(subreddits=list_subreddits_data, \
            start_date=self.st_dt, end_date=self.end_dt)
        if len(downloaded_subs) > 0:
            urls = list(set(urls)- set(downloaded_subs))
            print("Already Dowloaded {} sub-reddits yet to download {} sub-reddits".format(len(downloaded_subs), len(urls)))
            print("Completed {}%".format(len(downloaded_subs)/len(urls)))

        return urls

    def get_tasks(self):
        subreddits = self.get_subreddits_links_to_build_task()
        task = []
        list_subreddits = list(self.chunks(l=subreddits, n=self.chunk_size))
        for chunk_ in range(len(list_subreddits)):
            task.append(Reddit_Comment_Task(subreddit_chunk=chunk_, sav_path=self.sav_path))

        return task, list_subreddits

default_config = Config()
tasks_reddit_api = Task_getter()
tasks, subreddit_chunks = tasks_reddit_api.get_tasks()
print(tasks)
luigi.build(tasks=tasks, workers=default_config.no_of_workers)


from reddit_search.reddit_search import RedditSearch
from reddit_data_extraction.base import Base
from reddit_data_extraction.extract import Extract
from config import Config

default_config = Config()
subreddit_save_path = default_config.subreddit_path
comment_save_path = default_config.comments_path
submission_save_path = default_config.submission_path
base_ = Base(subreddit_json_path=subreddit_save_path)

# Intializing the Reddit Search API
reddit_search_obj = RedditSearch(save_path=subreddit_save_path)

# Intializing the comment and submission extract object - Pushshift API
comment_extract_obj = Extract(extract_source="comments", save_path=comment_save_path)
submission_extract_obj = Extract(extract_source="submission", save_path=submission_save_path)

# Extraction of Relevant subreddits based on the keywords
reddit_search_obj.reddit_search_all_keywords()

# get the list of subreddits for extraction of comments and submissions
subreddits = base_.get_data_list_subreddits()
subreddits = subreddits[0:3]

# Extraction of comments
comment_extract_obj.start_extraction(subreddits=subreddits)

# Extraction of submissions
submission_extract_obj.start_extraction(subreddits=subreddits)





class Config(object):

    start_date = "01-05-2020"
    end_date = "31-05-2020"

    # Keywords to search
    keywords = ["car", "kia seltos", "kia carnival"]

    # Output paths base path to save all the file downloaded (Local)
    output_base_path = "/home/arunachalam/Documents/sense2vec_exp/output_api"

    # Standardized paths
    subreddit_path = "{}/subreddit_extracted".format(output_base_path)
    comments_path = "{}/subreddit_comments".format(output_base_path)
    submission_path = "{}/subreddit_submission".format(output_base_path)

    # Reddit Credentials - Reddit API
    refresh_token_time = 3200
    x_rate_limit_per_min = 30 
    user_name = "instigateideas"
    password = "BugsLife@123"
    access_key = "MiQp8jSf4Zo3aw"
    secret_key = "YvtlQy5-5gZT_3dYcotW1rWwEHo"

    # Reddit Extraction - Pushshift API
    x_rate_limit_per_min_pushapi = 100

    # Extract what data submission or comments
    source_data = "comments"  # submission or comments

    # API Parameters
    size = 500
    epochs_delta = 86400*16

    # Host address (VPN or ECS) -> return should be JSON
    # host_address = "http://localhost:5555/get_html_content"
    host_address = "http://internal-reddit-alb-1748639389.us-east-2.elb.amazonaws.com/request_reddit_data"

    # Subreddits file saved path
    subreddit_json_path = "/home/arunachalam/Documents/sense2vec_exp/reddit_api/data"

    # Luigi Parameters
    no_of_workers = 3
    chunk_size = 10000

    # Resume file path
    resume_file = "/home/arunachalam/Documents/sense2vec_exp/resume.txt"

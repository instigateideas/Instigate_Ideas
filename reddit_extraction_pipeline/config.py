class Config(object):

    start_date = "01-10-2019"
    end_date = "31-10-2019"

    # Keywords to search
    keywords = ["car", "kia seltos", "kia carnival"]

    # Extract base path
    base_output_path = "/home/arunachalam/Documents/sense2vec_exp/ouputs"

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

    # Output Comment Extraction Path (Local)
    output_path = "/home/arunachalam/Documents/sense2vec_exp/reddits_comments_data_link"

    # API Parameters
    size = 500
    epochs_delta = 300

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

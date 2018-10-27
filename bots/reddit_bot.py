import praw
import sql_handler
import json

config = json.load(open('config.json'))

r = praw.Reddit(username=config['r_name'],
                password=config['r_pass'],
                client_id=config['r_client_id'],
                client_secret=config['r_client_secret'],
                user_agent="Dad Jokes sweeper V0.1")


def get_jokes():
    for post in r.subreddit('dadjokes').hot(limit=100):
        sql_handler.insert_joke(post_id=post.id, title=post.title, body=post.selftext, author=post.author)


get_jokes()

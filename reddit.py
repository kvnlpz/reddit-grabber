import string
import praw
import sys
import os.path
import discord
import asyncio
import time
import re
import base64
from github import Github
from github import InputGitTreeElement
import sys,os
from datetime import date
import yaml


conf = yaml.load(open('redditAPI.yml'))

reddit_client_id = conf['reddit']['clientID']
reddit_client_secret = str(conf['reddit']['clientSecret'])
reddit_user_agent = conf['reddit']['userAgent']
user = conf['github']['user']
password = conf['github']['password']
token = conf['github']['token']


g = Github(token)


# reddit = praw.Reddit(reddit_client_id, reddit_client_secret, reddit_user_agent)
reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret,
                         user_agent=reddit_user_agent)

subreddit_names = ""


def create_file_and_send(post_url, post_title):

    # YY-mm-dd
    todays_date = date.today()
    t = time.localtime()
    # current_time = time.strftime("%H:%M:%S", t)
    current_time = int(time.time())
 


    file_title = "" + str(todays_date) + "-reddit-" + str(current_time) + ".markdown"
   


  
    string_to_write = "--- \nlayout: post \ntitle: " + post_title + " \ndate: " + str(todays_date) + " " + str(current_time) + " \ncategories: reddit \n--- "

    string_to_write = string_to_write + "\n" + post_url

    user = g.get_user()

    repo = g.get_repo('kvnlpz/RSSFeed')  # repo name

    print("getting labels")

    labels = repo.get_labels()

    repo.create_file("_posts/" + file_title, "reddit update", string_to_write, branch="main")


path_to_file = os.path.abspath("subreddit_list.txt")
# create the file if it doesnt exist already
f = open(path_to_file, "r+")

sub_list = list(f)

for i in sub_list:
    # check fo see if
    if sub_list.index(i) != len(sub_list) - 1:
        subreddit_names = subreddit_names + i + "+"
    else:
        subreddit_names = subreddit_names + i
    f.close()

print(subreddit_names)
subreddits = reddit.subreddit(subreddit_names)
mysubmissions = subreddits.stream.submissions(skip_existing=True)
start_time = time.time()
subreddits = reddit.subreddit(subreddit_names)

while (True):
    try:
        mysubmissions = subreddits.stream.submissions(skip_existing=True)
        start_time = time.time()
        submission = next(mysubmissions)
        if submission is None:
            # Wait 60 seconds for a new submission
            time.sleep(60)
        else:
            print("recieved submission from " + submission.subreddit.display_name.lower())
            create_file_and_send(submission.shortlink, submission.title)
            time.sleep(2)

    except:
        print("An exception occurred")
        time.sleep(50)
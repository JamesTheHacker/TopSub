#!/usr/bin/env python

import argparse
import ConfigParser
import logging
import praw
import os

# Fetch a top submission from a subreddit
def topSubmissions(reddit, sub, limit=5):
    submissions = reddit.subreddit(sub).hot(limit=5)
    return [submission for submission in submissions if not submission.stickied]

# Post a URL on the specified sub
def repostURL(reddit, sub, title, url):
    reddit.subreddit(sub).submit(
        title=title,
        url=url,
        resubmit=False
    )    

# Main function ... self explanatory
def main(args, logger, config):

    # Create new praw instance
    reddit = praw.Reddit(
        client_id=config.get('praw', 'client_id'),
        client_secret=config.get('praw', 'client_secret'),
        password=config.get('praw', 'password'),
        user_agent=config.get('praw', 'user_agent'),
        username=config.get('praw', 'username')
    )

    # Get top submissions from sub
    submissions = topSubmissions(reddit, args.subreddit)
    
    # Loop through submissions. If submission has already been submitted try another
    for submission in submissions:
        try:
            repostURL(reddit, args.postsub, submission.title, submission.url)
            break
        except praw.exceptions.APIException, e:
            logger.info(e)
            continue
        except Exception, e:
            logger.warning(e)
            

if __name__ == "__main__":
    
    # Argparser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subreddit', required=True, help='Subreddit to scrape')
    parser.add_argument('-p', '--postsub', required=True, help='Subreddit to post to')
    parser.add_argument('-c', '--config', required=True, help='Path to config file')
    args = parser.parse_args()

    # Setup logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Load config file
    config = ConfigParser.ConfigParser()
    config.read(args.config)

    main(args, logger, config)


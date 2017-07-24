#!/usr/bin/env python

import argparse
import ConfigParser
import logging
import praw

# Fetch a top submission from a subreddit
def topSubmissions(reddit, sub, top_filter):
    submissions = reddit.subreddit(sub).top(top_filter)
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
    submissions = topSubmissions(reddit, args.subreddit, args.filter)
    
    # Loop through submissions. If submission has already been submitted try another
    for submission in submissions:
        try:
            repostURL(reddit, args.postsub, submission.title, submission.url)
            break
        except praw.exceptions.APIException, e:
            logger.info(e)
        except Exception, e:
            logger.warning(e)
            

if __name__ == "__main__":
    
    # Argparser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subreddit', required=True, help='Subreddit to scrape')
    parser.add_argument('-p', '--postsub', required=True, help='Subreddit to post to')
    parser.add_argument('-c', '--config', required=True, help='Path to config file')
    parser.add_argument('-f', '--filter', required=False, default='week', help='Top filter: all, day, hour, month, week, year')
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


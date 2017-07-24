#TopSub

TopSub is a Reddit script that allows you to repost/cross post content on your own sub. This is useful for create subs that archive "top" content. Here's an example of a subreddit ran by the author [/r/topjokes](https://www.reddit.com/r/topjokes/).

##Installing

    git clone http://github.com/JamesTheHacker/TopSub
    cd TopSub
    pip install -r requirements.txt

##Configuration

Modify `praw.conf`:

    [praw]
    client_id=
    client_secret=
    password=
    user_agent=
    username=

##Running

    ./topsub.py --subreddit jokes --postsub topjokes --config praw.conf

* `--subreddit` is the subreddit you want to take top posts from.
* `--postsub` is the subreddit you want to repost to
* `--config` should contain the path to your config file

##Recommendations

I run this script on a cronjob. I run multiple subs using different accounts so I like to pass in different config files for different accounts.

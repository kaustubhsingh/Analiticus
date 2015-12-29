from flask import Flask, render_template

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

import tweepy
import re
import os
import sqlite3
from flask import g


app = Flask(__name__)

@app.route('/')
def home():

    g.db = sqlite3.connect("tweets.db")

    g.db.execute("DROP TABLE IF EXISTS tweets")
    g.db.execute("CREATE TABLE tweets ( tweet TEXT );")

    with open('oauth.txt') as f:
        credentials = [x.strip() for x in f.readlines()]

    ckey=credentials[0]
    csecret=credentials[1]
    atoken=credentials[2]
    asecret=credentials[3]
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    api = tweepy.API(auth)

    query = 'california'
    max_tweets = 15
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]

    for tweet in searched_tweets:
        split_result = re.split(r',', str(tweet))
        print split_result[2]
        print    
        loc = str(tweet).split("location': u'")
        loc = loc[1].split(",")
        loc = loc[0].split("'")
        print loc[0]
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
        
        g.db.execute("INSERT INTO tweets VALUES (?)", [split_result[2]])
        g.db.commit()


    if hasattr(g, 'db'):
        g.db.close()

    return 

if __name__ == '__main__':
    app.run(debug=True)
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
    g.db.execute("CREATE TABLE tweets ( tweet TEXT, location TEXT );")

    with open('oauth.txt') as f:
        credentials = [x.strip() for x in f.readlines()]

    ckey=credentials[0]
    csecret=credentials[1]
    atoken=credentials[2]
    asecret=credentials[3]
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    api = tweepy.API(auth)

    query = 'trump'
    max_tweets = 500
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]

    l = dir(searched_tweets[0].user)
    print l
        
    for tweet in searched_tweets:
              
        print tweet.text.encode('utf-8')
        print tweet.user.location.encode('utf-8')
            
        g.db.execute("INSERT INTO tweets VALUES (?, ?)", [tweet.text, tweet.user.location])      
        g.db.commit()

    if hasattr(g, 'db'):
        g.db.close()

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
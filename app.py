from flask import Flask, render_template, request

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

@app.route('/', methods=['GET', 'POST'])
def home():

    tweet_list = list()
    
    if request.method == "POST":
        # get keyword that the user has entered
        keyword = request.form['keyword']
        
       
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
    
        query = keyword
        max_tweets = 50
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]
    
        l = dir(searched_tweets[0].user)
        print l
            
        for tweet in searched_tweets:      
            print tweet.text.encode('utf-8')
            tweet_list.append(tweet.text)
            
            print tweet.user.location.encode('utf-8')
                
            g.db.execute("INSERT INTO tweets VALUES (?, ?)", [tweet.text, tweet.user.location])      
            g.db.commit()
    
        if hasattr(g, 'db'):
            g.db.close()
        return render_template('index.html', tweets=keyword)
    return render_template('index.html', tweets=tweet_list)


if __name__ == '__main__':
    app.run(debug=True)
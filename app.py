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
try:
    import oauth
except ImportError:
    import os
import sentiment    
    
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    tweet_list = list()
    
    if request.method == "POST":
        # get keyword that the user has entered
        keyword = request.form['keyword']
        if keyword == "":
                return render_template('index.html', tweets=tweet_list)
      
        g.db = sqlite3.connect("tweets.db")
    
        g.db.execute("DROP TABLE IF EXISTS tweets")
        g.db.execute("CREATE TABLE tweets ( tweet TEXT, location TEXT, score INT );")
 
        ckey   = os.environ['ckey']
        csecret= os.environ['csecret']
        atoken = os.environ['atoken']
        asecret= os.environ['asecret']
   
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

   
        api = tweepy.API(auth)
  
        query = keyword
        max_tweets = 50
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]
      
        print dir(searched_tweets[0])
        for tweet in searched_tweets:      
            #print tweet.text.encode('utf-8')
            tweet_list.append(tweet.text)
            
            #print tweet.user.location.encode('utf-8')
                
            g.db.execute("INSERT INTO tweets VALUES (?, ?)", [tweet.text, tweet.user.location])      
            g.db.commit()
    
        data = g.db.execute("SELECT DISTINCT location from tweets")
    
        viewlist = []
        for row in data:
            #print row
            viewlist.append(row[0])
            
            
        if hasattr(g, 'db'):
            g.db.close()

    return render_template('index.html', tweets=viewlist)


if __name__ == '__main__':
    app.run(debug=True)
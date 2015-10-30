from flask import Flask, render_template

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

import tweepy
import re

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    # return "Hello! Welcome to Analiticus" 

    with open('oauth.txt') as f:
        credentials = [x.strip() for x in f.readlines()]

    ckey=credentials[0]
    csecret=credentials[1]
    atoken=credentials[2]
    asecret=credentials[3]
    
    #class listener(StreamListener):
    
    #    def on_data(self, data):
            
    #        decoded = json.loads(data)
            
    #        print '%s    %s' % (decoded['text'].encode('ascii', 'ignore'), decoded['user']['location'])
    #        return(True)
    
    #    def on_error(self, status):
    #        print status
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    #twitterStream = Stream(auth, listener())
    #twitterStream.filter(track=['bmw'])
    
    api = tweepy.API(auth)

    query = 'kejriwal'
    max_tweets = 10
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]

    for tweet in searched_tweets:
        split_result = re.split(r',', str(tweet))
        print split_result[2]

    

    return 


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

import tweepy
import re

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

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

    query = 'Hilton Hotels'
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
        
        #i = 0
        #for k in split_result:
        #    print i
        #    print k
        #    i = i + 1

    

    return 


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
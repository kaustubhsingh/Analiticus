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
import similar

from flask_mail import Mail, Message

#import logging

app = Flask(__name__)

import email

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'smajik23@gmail.com'
app.config['MAIL_PASSWORD'] = 'smajiksmajik'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


#app.logger.addHandler(logging.StreamHandler())
#app.logger.setLevel(logging.ERROR)
    
@app.route('/', methods=['GET', 'POST'])
def home():

    viewlist      = list()
    viewlocations = list()
    viewscores    = list()
    pos_tweets    = list()
    pos_tweet_locations = list()
    neg_tweets    = list()
    neg_tweet_locations = list()
    error         = ""
    donut_chart_data = list()
    pos_score     = 0;
    pos_percent   = 0
    keyword       = ""

    
    if request.method == "POST":
        # get keyword that the user has entered
        keyword = request.form['keyword']
        if keyword == "":
                return render_template('index.html')
      
        g.db = sqlite3.connect("tweets.db")
    
        g.db.execute("DROP TABLE IF EXISTS tweets")
        g.db.execute("CREATE TABLE tweets ( tweet TEXT, location TEXT, score REAL );")
 
        ckey   = os.environ['ckey']
        csecret= os.environ['csecret']
        atoken = os.environ['atoken']
        asecret= os.environ['asecret']
   
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

   
        api = tweepy.API(auth)
  
        query = keyword
        max_tweets = 200
        
        try:
            searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]
                
            #print dir(searched_tweets[0])
            pos_score = 0
            neg_score = 0
            neu_score = 0
            
            for tweet in searched_tweets:      
                #print tweet.text.encode('utf-8')
                viewlist.append(tweet.text)
                
                #score = 1
                score = sentiment.tweet_score(tweet.text)
                if score > 0.01:
                    pos_score += 1
                elif score < -0.01:
                    neg_score += 1
                else:
                    neu_score += 1
                
                g.db.execute("INSERT INTO tweets VALUES (?, ?, ?)", [tweet.text, tweet.user.location, score])      
            

            # Save sentiment data for visualization
            pos_percent = int(round(float(pos_score) / (pos_score + neg_score + neu_score) * 100, 0))
            neg_percent = int(round(float(neg_score) / (pos_score + neg_score + neu_score) * 100, 0))
            neu_percent = int(round(float(neu_score) / (pos_score + neg_score + neu_score) * 100, 0))
            
            donut_chart_data = [ pos_percent, neu_percent, neg_percent]
            #print json.dumps(donut_chart_data)
            
            # most positive tweets
            positive_tweets_data = g.db.execute("SELECT tweet, location FROM tweets WHERE score > 0.01 ORDER BY score DESC LIMIT 50")
            pos_count = 0
            for row in positive_tweets_data:
                #print row
                if pos_count < 10 and row[0] not in pos_tweets:
                    if similar.not_similar(row[0], pos_tweets):
                        pos_tweets.append(row[0])
                        pos_tweet_locations.append(row[1])
                        pos_count +=1
    
            # most negative tweets
            negative_tweets_data = g.db.execute("SELECT tweet, location FROM tweets WHERE score < -0.01 ORDER BY score ASC LIMIT 50")
            neg_count = 0
            for row in negative_tweets_data:
                #print row
                if neg_count < 10 and row[0] not in neg_tweets:
                    if similar.not_similar(row[0], neg_tweets):
                        neg_tweets.append(row[0])
                        neg_tweet_locations.append(row[1])
                        neg_count += 1
                
            if hasattr(g, 'db'):
                g.db.commit()
                g.db.close()
        
        except IOError:
            error = "Twitter Search API's rate limit exceeded. Please try after some time!"
            
    return render_template('index.html',
                           keyword    =  keyword,
                           pos_score  =  pos_percent,
                           donut_chart_data = json.dumps(donut_chart_data),
                           tweets     =  viewlist,
                           locations  =  viewlocations,
                           scores     =  viewscores,
                           pos_tweets =  pos_tweets,
                           pos_tweet_locations =  pos_tweet_locations,
                           neg_tweets =  neg_tweets,
                           neg_tweet_locations =  neg_tweet_locations,
                           error      = error
                           )

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')





mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        
        #print (app.config['MAIL_PORT'])
        print ("testing!")
        
        msg = Message("Message from your visitor",
                          sender='KS',
                          recipients=['smajik23@gmail.com'])
        '''
        msg.body = """
            From: %s <%s>,
            %s
            """ % (request.form['yourname'], request.form['youremail'], request.form['yourmessage'])
        mail.send(msg) '''
        
        msg.body = "testing"
        mail.send(msg)
             
        return render_template('thanks.html')
    elif request.method == 'GET':
        return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)

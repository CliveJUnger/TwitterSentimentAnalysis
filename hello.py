from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import tweepy
import textblob
import re
from datetime import datetime
import api_keys

app = Flask(__name__)

@app.route("/")
def input():
    return render_template("layout.html")

@app.route("/tweet", methods=['POST'])
def tweet():
    consumer_key = api_keys.consumer_key
    consumer_secret = api_keys.consumer_secret
    access_token = api_keys.access_token
    access_token_secret = api_keys.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stock = request.form["stock"]
    api = tweepy.API(auth)
    newTweets = []
    avg = 0
    count = 0
    followerMult = 0.1
    rtMult = 0.2
    public_tweets = api.search(q = stock, count = 500)

    for tweet in public_tweets:
        test = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
        blob = textblob.TextBlob(test)
        if blob.sentiment.polarity != 0:
            avg += blob.sentiment.polarity
            count += 1
            newTweets.append(tweet)
            print(blob.sentiment.polarity)
            print(test)

    newestTweet = newTweets[0].created_at
    oldestTweet = newTweets[count-1].created_at
    timedelta = newestTweet - oldestTweet
    print("tweets in the last:", timedelta, "minutes.")
    avg /= count
    print("average:", avg)
    return render_template('tweet.html', **locals())



if __name__ == "__main__":
    app.run()

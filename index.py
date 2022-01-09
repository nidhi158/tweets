# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import preprocessor as p
import tweepy
import json
import pandas as pd
import datetime
from gensim.parsing.preprocessing import remove_stopwords
import matplotlib.pyplot as plt
consumer_key = "aFwXJjhQrb6TFIKk0N4DynmQ4"
consumer_secret = "qjiOyBFqReUo3mQtfttOJQhtTpXuZPJrAiQD6uOmCZ45cuxHD9"
access_token = "1097468063446900736-YJHWkhMg4rQtUlunbxj46AQFEPWF7H"
access_token_secret = "fnKA19CSSHaPvsLMVIC6h8LC3lPGk3qW7OQwwTnsRgMW2"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


# foreach through all tweets pulled
def display(public_tweets):
    for tweet in public_tweets:
        print (tweet.text)

#display(public_tweets)

def searchTweet():
    search_words = "#covid"
    date_since = "2021-05-05"
    tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(5)
    for tweet in tweets:
        print(tweet.text)


#searchTweet()

def Location():
    search_words = "covid"
    date_since = "2021-05-05"
    tweets = tweepy.Cursor(api.search,
                           q=search_words,
                           lang="en",
                           since=date_since).items(5)
    users_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]
    tweet_text = pd.DataFrame(data=users_locs,
                    columns=['user', "location"])
    print(tweet_text)

#Location()


def storecsv():
    today = datetime.date.today()
    yesterday= today - datetime.timedelta(days=1)
    tweets_list = tweepy.Cursor(api.search, q="#Covid-19 since:" + str(yesterday)+
                                              " until:" + str(today),tweet_mode='extended', lang='en').items(50)
    output = []
    for tweet in tweets_list:
        text = tweet._json["full_text"]
        #print(text)
        favourite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        created_at = tweet.created_at

        line = {'text': text, 'favourite_count': favourite_count, 'retweet_count': retweet_count,
                'created_at': created_at}
        output.append(line)
        #print(line)

    df = pd.DataFrame(output)
    print(df)
    df.to_csv('output.csv')

#storecsv()

def preprocess_tweet(row):
    text = row['text']
    text = p.clean(text)
    return text

def stopword_removal(row):
    text = row['text']
    text = remove_stopwords(text)
    return text

def process():
    train_df=pd.read_csv('output.csv')
    train_df = train_df.dropna()
    train_df = train_df.drop_duplicates()
    train_df['text'] = train_df.apply(preprocess_tweet, axis=1)
    train_df['text'] = train_df.apply(stopword_removal, axis=1)
    train_df['text'] = train_df['text'].str.lower().str.replace('[^\w\s]', ' ',regex=True).str.replace('\s\s+', ' ',regex=True)
    print(train_df.count())
    print(train_df.text)

process()

def postTweet(text):
    status = api.update_status(status=text)

#postTweet("Hello world")



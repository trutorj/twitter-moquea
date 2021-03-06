import tweepy 
import os
from dotenv import load_dotenv

#Add your credentials here
load_dotenv()
twitter_keys = {
        'consumer_key': os.getenv('API_KEY'),
        'consumer_secret': os.getenv('API_SECRET'),   
        'access_token_key': os.getenv('ACCES_TOKEN'),
        'access_token_secret': os.getenv('ACCESS_TOKEN_SECRET')
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

# Search parameters
search_term = "gramíneas"
tweets = tweepy.Cursor(api.search, 
                   q= search_term,
                   lang="es",
                   since="2020-05-18").items(1000)

all_tweets = [tweet.place for tweet in tweets]

#Make call on home timeline, print each tweets text
#public_tweets = api.home_timeline()
#for tweet in api.search('gramíneas, alergia'):
#    print(tweet.text)

all_tweets[:5]
import GetOldTweets3 as got
import pandas as pd
import re

# Adapted from:
# https://gitlab.com/praj88/twitter-analytics/blob/master/scripts/twitter-analytics.ipynb

# Extract tweets based in location, date range and specific keywords:

def extractorTweets(search_terms, date_start, date_end, location):
    tweet_df_all = pd.DataFrame()
    for term in search_terms:
        print('Looking for', term)
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(term)\
                                               .setSince(date_start)\
                                               .setUntil(date_end)\
                                               .setNear(location)\
                                               .setWithin("50km") # más o menos 50 km
        tweet = got.manager.TweetManager.getTweets(tweetCriteria)
        tweet_list = [[tweet[x].id,
                      tweet[x].author_id,
                      tweet[x].text,
                      tweet[x].retweets,
                      tweet[x].permalink,
                      tweet[x].date,
                      tweet[x].formatted_date,
                      tweet[x].favorites,
                      tweet[x].mentions,
                      tweet[x].hashtags,
                      tweet[x].geo,
                      tweet[x].urls
                 ]for x in range(0, len(tweet))]
        tweet_df = pd.DataFrame(tweet_list)
        tweet_df['search_term'] = term
        tweet_df_all = tweet_df_all.append(tweet_df)
    tweet_df_all.columns = ['id','author_id','text','retweets','permalink','date','formatted_date','favorites','mentions','hashtags','geo','urls', 'search_term']
    return tweet_df_all

# Function to clean the data
def limpiador(df):
    # Clean all the tweets with 'alegría' 
    df = df[df.text.str.contains('[Aa]legr|ALEGR', regex=True)==False]
    # Clean all the tweets with the user name containing 'alegría' or related
    df = df[df.permalink.str.contains('[Aa]legr', regex=True)==False]
    # Delete duplicated tweets by its id
    df = df.drop_duplicates(subset ="id", inplace = True) 
    return df


import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
#from nltk.corpus import wordnet
#guidence from tutorial: https://www.youtube.com/watch?v=jtIMnmbnOFo
#using python wrapper
#allows pandas to show the full text of the tweets
pd.set_option('display.max_colwidth', None)
#function def
def scrape(keyword, num_tweets, start_date, end_date):
    #construct the query
    query = keyword + ' since:' + start_date + ' until:' + end_date
    #getting synonyms to the keyword to use in search
    #keywords = wn.synsets(keyword)[0]
    tweets = []
    #max number of tweets to collect (could be less if there aren't that many results)
    limits = num_tweets
    print(query)
    data = sntwitter.TwitterSearchScraper(query).get_items()
    for i, tweet in enumerate(data):
        if i >= limits:
            break
        else:
            tweets.append([tweet.content, tweet.date, tweet.user.username])
 
    df_1 = pd.DataFrame(tweets, columns=['Tweet', 'Date', 'User' ])
    #removes duplicate entries
    df_1.drop_duplicates()
    #removes duplicate users
    df_1.drop_duplicates(subset=['User'])
    #number of tweets to add to the data frame inorder to make up for the removed duplicates
    num_tweets_toadd = num_tweets - len(df_1)
    #holder array for replacements tweets
    tweets_replace_duplicates = []
    #collects replacement data
    for i, tweet in enumerate(data):
        if i >= num_tweets_toadd:
            break
        else:
            tweets_replace_duplicates.append([tweet.content, tweet.date, tweet.user.username])
    df_2 = pd.DataFrame(tweets_replace_duplicates, columns=['Tweet', 'Date', 'User' ])
    #print(df_1['Tweet'].iloc[0] == df_2['Tweet'].iloc[0])
    #combines the origional data with the replacement data
    df_final = pd.concat([df_1,df_2])
    print(df_final.shape[0])
    print(df_1.shape[0])
    print(df_2.shape[0])
    return df_final.to_csv()
 
scrape("e", 500, '2021-10-05', '2022-10-06')
 
 
#using CIL
#creates seprate json file, then converts to df then to csv, less efficent
def os_scrape(keyword, num_tweets, start_date, end_date):
    os.system(f"snscrape --jsonl --max-results {num_tweets} --since {start_date} twitter-search '{keyword}' > tweets.json")
    df = pd.read_json("tweets.json", lines=True)
    print (df.keys())
    df = df[['date', 'user', 'content']]
    return df.to_csv
#os_scrape("computers", 200, '2021-01-12', '2022-01-05')

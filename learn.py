import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
#import wordnet as wn
#guidence from tutorial: https://www.youtube.com/watch?v=jtIMnmbnOFo
#using python wrapper
def scrape(keyword, num_tweets, start_date, end_date):
    query = keyword + ' since:' + start_date + ' until:' + end_date
    #getting synonyms to the keyword to use in search
    #keywords = wn.synsets(keyword)[0]
    tweets = []
    #max number of tweets to collect
    limits = num_tweets
    print(query)
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > limits:
            break
        else:
            tweets.append([tweet.date, tweet.user.username, tweet.content])
 
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    return df.to_csv()
 
scrape("computers", 200, '2021-01-12', '2022-01-05')
 
 
#using CIL
#creates seprate json file, then converts to df then to csv, less efficent
def os_scrape(keyword, num_tweets, start_date, end_date):
    os.system(f"snscrape --jsonl --max-results {num_tweets} --since {start_date} twitter-search '{keyword}' > tweets.json")
    df = pd.read_json("tweets.json", lines=True)
    print (df.keys())
    df = df[['date', 'user', 'content']]
    return df.to_csv
os_scrape("computers", 200, '2021-01-12', '2022-01-05')



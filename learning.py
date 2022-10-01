import snscrape.modules.twitter as sntwitter
import pandas as pd

#guidance from tutorials: https://www.youtube.com/watch?v=QLIYJoRvd-M https://www.youtube.com/watch?v=jtIMnmbnOFo

#user inputs what they want
keyword = input('Enter a keyword: ')
num_tweets = int(input('How many tweets do you want to scrape? '))
since = input('Since (yyyy-mm-dd): ')
until = input('Until (yyyy-mm-dd, this is exclusive): ')

query = keyword + ' since:' + since + ' until:' + until #the same way you would input a query in twitter itself
print(query)
tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > num_tweets:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content, tweet.url])
 
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'URL'])
df.to_csv()
print(df)
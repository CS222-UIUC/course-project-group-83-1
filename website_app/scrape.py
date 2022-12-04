import snscrape.modules.twitter as sntwitter
import pandas as pd
from nltk.corpus import wordnet
from cleantext import clean #need to install clean-text library beforehand

import datetime
#install unidecode
'''
generate_keys returns a list of keywords (strings) 
that are related to the string passed into the fuction.
The returned list will always contain the string that
was passed in. There may be problems if the user 
passes in an underscore as the word used to generate
words.
'''
def generate_keys(word):
    keywords = wordnet.synsets(word)[0].lemma_names()
    for i in range(len(keywords)):
        keywords[i] = keywords[i].replace('_',' ')
    return keywords

'''
Same function as above, but does not remove underscores.
Will probably need to check if the initial word passed in
contains an underscore and then decide which key generation
function to use.
'''
def generate_keys_(word):
    keywords = wordnet.synsets(word)[0].lemma_names()
    return keywords

'''
clean_up removes emojis, urls, and other data from the tweet
that may interfere with the semantic analysis process.
More factors to consider will be added as deeemed necessary

by the team.
'''
def clean_up(text):
    text = clean(text, no_urls=True, replace_with_url="",no_emoji=True)
    text = text.replace('@', '')
    text = text.replace('\n', '')
    #will add more as deemed necessary for semantic analysis
    return text

'''
keyword: keyword used to search
start_date: date to start seaching in year-month-day format xxxx-xx-xx
end_date: date to stop seaching in year-month-day format xxxx-xx-xx

output_file: filename to write results to

Scrapes tweets related to a given keyword between a specific
time frame. Cleans tweets of content that may interfere with
semantic analysis. Removes duplicate entries and duplicate users. 
Writes results as a JSON file named tweets.json.
This function can take between 15-60 minutes to complete since
it collects ALL tweets between the time range.
Note: orignally this fuction took in a list of keywords. However
after further investigation, snscrape does not directly search
with the keyword (some tweets collected do not contain the 
exact keyword). This fuction was changed back to only searching
with one keyword. Going foward, in the user interface, the related
keys should be generated and the user should be promted to pick one
that will be used in the query.
'''

def scrape(keyword, start_date, end_date, output_file):
    tweets = []
    query = keyword + ' since:' + start_date + ' until:' + end_date
    data = sntwitter.TwitterSearchScraper(query).get_items()
    for tweet in data:
            tweets.append([clean_up(tweet.content), tweet.date, tweet.user.username])
    df_1 = pd.DataFrame(tweets, columns=['Tweet', 'Date', 'User' ])
    df_1.drop_duplicates()
    df_1.drop_duplicates(subset=['User'])
    print(df_1)
    with open(output_file, "w") as f:
        f.write(df_1.to_json())

'''
This function is the same as above except that it
only collects a certain amount of tweets per day in the given date range.
This function will be used for testing 
purposes since it is not practical to run 15-60 minute
tests often.
Note: I had two ideas for trying to scarpe x amount of tweets per day.
One was to query each day in the date range
and add 200 tweets from each day to the data.
Another was to query the entire date range
but only save x amount of tweets from each date.
I don't know if one is more efficient than the other
as I'm still trying to figure out the second approach
'''
def scrape_twitter(keyword, start_date, end_date, output_file):
    tweets = []
    # query = keyword + ' since:' + start_date + ' until:' + end_date
    # data = sntwitter.TwitterSearchScraper(query).get_items()
    # current_date = datetime.date.fromisoformat(end_date) - datetime.timedelta(1)
    # for i, tweet in enumerate(data):
    #     if (tweet.date.date() != current_date):
    #         continue
    #     if i < 4:
    #         tweets.append([clean_up(tweet.content), tweet.date, tweet.user.username])
    #     else:
    #         current_date = current_date - datetime.timedelta(1)
    #         i = 0
    end_interval = datetime.date.fromisoformat(end_date)
    start_interval = end_interval - datetime.timedelta(1)
    while (end_interval != datetime.date.fromisoformat(start_date)):
        query = keyword + ' since:' + datetime.date.isoformat(start_interval) + ' until:' + datetime.date.isoformat(end_interval)
        data = sntwitter.TwitterSearchScraper(query).get_items()
        for i, tweet in enumerate(data):
            if i >= 200:
                break
            else:
                tweets.append([clean_up(tweet.content), tweet.date, tweet.user.username])
        end_interval = end_interval - datetime.timedelta(1)
        start_interval = start_interval - datetime.timedelta(1)
    df_1 = pd.DataFrame(tweets, columns=['Tweet', 'Date', 'User' ])
    df_1 = df_1.drop_duplicates()
    df_1 = df_1.drop_duplicates(subset=['User'])
    print(df_1)
    with open(output_file, "w") as f:
        f.write(df_1.to_json())

# renamed scrape_test to scrape_twitter 
#scrape_test("abortion", "2022-04-25", "2022-05-09", "abortion.json")
#scrape_test("voter fraud", "2020-11-01", "2020-11-08", "voter fraud.json")

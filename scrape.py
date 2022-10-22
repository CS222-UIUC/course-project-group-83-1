import snscrape.modules.twitter as sntwitter
import pandas as pd
from nltk.corpus import wordnet
from cleantext import clean  # need to install clean-text library beforehand
import data_clean

"""
generate_keys returns a python list of words (strings)
that are related to the string passed into the fuction.
The returned list will always contain the string that
was passed in. There may be problems if the user
passes in an underscore as the word used to generate
words.
"""


def generate_keys(word):
    keywords = wordnet.synsets(word)[0].lemma_names()
    for i in range(len(keywords)):
        keywords[i] = keywords[i].replace("_", " ")
    return keywords


"""
Same function as above, but does not remove underscores.
Will probably need to check if the initial word passed in
contains an underscore and then decide which key generation
function to use.
"""


def generate_keys_(word):
    keywords = wordnet.synsets(word)[0].lemma_names()
    return keywords


"""
clean_up removes emojis, urls, and other data from the tweet
that may interfere with the semantic analysis process.
more factors to consider will be added as deeemed necessary
by the team.
"""


def clean_up(text):
    text = clean(text, no_urls=True, no_emoji=True, replace_with_url="")
    return data_clean.cleanTweets(text)


"""
keyword_list: list of words generated to search
start_date: date to start seaching in year-month-day format xxxx-xx-xx
end_date: date to stop seaching in year-month-day format xxxx-xx-xx
takes in a list of words to scrape tweets between a specific
time frame. Removes duplicate entries and duplicate users.
Writes results as a JSON file named tweets.json.
This function can take between 15-60 minutes to complete since
it collects ALL tweets between the time range.
"""


def scrape(keyword_list, start_date, end_date):
    tweets = []
    for keyword in keyword_list:
        query = keyword + " since:" + start_date + " until:" + end_date
        data = sntwitter.TwitterSearchScraper(query).get_items()
        for tweet in data:
            tweets.append(
                [clean_up(tweet.content), tweet.date, tweet.user.username]
            )  # noqa
    df_1 = pd.DataFrame(tweets, columns=["Tweet", "Date", "User"])
    df_1.drop_duplicates()
    df_1.drop_duplicates(subset=["User"])
    f = open("tweets.json", "w")
    f.close()
    f.write(df_1.to_json())


"""
This function is the same as above except that it
stops collecting tweets once a certian amount of data
is collected. This function will be used for testing
purposes since it is not practical to run 15-60 minute
tests often.
"""


def scrape_test(keyword_list, start_date, end_date):
    tweets = []
    for keyword in keyword_list:
        query = keyword + " since:" + start_date + " until:" + end_date
        data = sntwitter.TwitterSearchScraper(query).get_items()
        for i, tweet in enumerate(data):
            if i >= 2:
                break
            else:
                tweets.append(
                    [clean_up(tweet.content), tweet.date, tweet.user.username]
                )
    df_1 = pd.DataFrame(tweets, columns=["Tweet", "Date", "User"])
    df_1 = df_1.drop_duplicates()
    df_1 = df_1.drop_duplicates(subset=["User"])
    f = open("tweets.json", "w")
    f.write(df_1.to_json())

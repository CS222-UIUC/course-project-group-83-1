import snscrape.modules.twitter as sntwitter
import pandas as pd

from textblob import TextBlob
from wordcloud import WordCloud
import re

import matplotlib.pyplot as plt
import seaborn as sns

from nltk.stem.snowball import SnowballStemmer
import spacy
nlp = spacy.load("en_core_web_sm")

tweets = []
n = 100
word = 'musk'
start = '2022-01-01'
# scraping twitter
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(word + ' since:' + start + ' until:{today}').get_items()):
    if i>n:
        break
    tweets.append([tweet.content])
    
tweets_to_df = pd.DataFrame(tweets, columns=['Tweets'])

# clean tweets using regex
def cleanTweets(text):
    text = re.sub('@[A-Za-z0-9_]+', '', text)   # remove @mentions
    text = re.sub('#','',text)                  # remove hashtags
    text = re.sub('RT[\s]+','',text)
    text = re.sub('https?:\/\/\S+', '', text)   # remove urls
    text = re.sub('\n',' ',text)
    return text

tweets_to_df['cleanedTweets'] = tweets_to_df['Tweets'].apply(cleanTweets)

tweets_to_df.to_csv('tweets.csv')                    # write df into csv file
savedTweets = pd.read_csv('tweets.csv', index_col=0) # read csv file

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

savedTweets['Subjectivity'] = savedTweets['cleanedTweets'].apply(getSubjectivity)
savedTweets['Polarity'] = savedTweets['cleanedTweets'].apply(getPolarity)

print(savedTweets.drop('Tweets', axis=1).head())

def getAnalysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'
    
savedTweets['Analysis'] = savedTweets['Polarity'].apply(getAnalysis)

# bar graph
colors = ['palegreen', 'lightgrey', 'lightcoral']
savedTweets['Analysis'].value_counts().plot(kind='bar',color=colors)
plt.title('Tweet Polarities')
plt.ylabel('Count')
plt.xlabel('Polarity')
plt.show()

# pie chart
savedTweets['Analysis'].value_counts().plot(kind='pie', colors=colors, startangle=90, label='')
plt.title('Distribution of Polarities')
plt.show()

# scatterplot
for i in range(0,savedTweets.shape[0]):
    plt.scatter(savedTweets['Polarity'][i],savedTweets['Subjectivity'][i])
plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

# word clouds
def create_wordcloud(text):    
    allWords = ' '.join([tweets for tweets in text])
    wordCloud = WordCloud(background_color='white').generate(allWords)
    plt.imshow(wordCloud)
    plt.axis('off')
    plt.show()

posTweets = savedTweets.loc[savedTweets['Analysis']=='Positive', 'cleanedTweets']
negTweets = savedTweets.loc[savedTweets['Analysis']=='Negative', 'cleanedTweets']
create_wordcloud(posTweets)
create_wordcloud(negTweets)

# tweets to words
sentences = []
for word in savedTweets['cleanedTweets']:
    sentences.append(word)
lines = []
for line in sentences:
    words = line.split()
    for w in words:
        lines.append(w)

# stem words to roots
stemmer = SnowballStemmer(language='english')
stem = []
for word in lines:
    stem.append(stemmer.stem(word))

# remove stopwords
stem2 = []
for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)

df = pd.DataFrame(stem2)
df = df[0].value_counts()

# top 20 used words
df = df[:20]
sns.barplot(x=df.values, y=df.index, alpha=0.8)
plt.title('Top Words')
plt.xlabel('frequencies', fontsize=12)
plt.ylabel('words', fontsize=12)
plt.show()
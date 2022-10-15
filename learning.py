import snscrape.modules.twitter as sntwitter
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
#snscrape/panda guidance from tutorials: https://www.youtube.com/watch?v=QLIYJoRvd-M https://www.youtube.com/watch?v=jtIMnmbnOFo
 
def adjustDate(date): #converts user inputted mm/dd/yy to yyyy-mm-dd (kind of hard-cody I know, can def be expanded later)
    if date[2] == '/':
        return '20'+date[6]+date[7]+'-'+date[0]+date[1]+'-'+date[3]+date[4]
    return date


def related(keyword): # gets the synonyms to the keyword and prints them https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
    sysnet = wn.synsets(keyword)
    synonyms = set()
    if len(sysnet) != 0:
        count = 0
        for syn in sysnet:
            for lemna in syn.lemmas():
                if (lemna.name() != keyword): 
                    synonyms.add(lemna.name()) #need to dig deeper in understanding what these lemnas are because some "synonyms" are kind of weird
                    count+=1
                if (count == 5): #limits synonyms to 5
                    break
            if (count == 5):
                break #surely there's a better way to do this... not familiar enough with python to know shortcuts
        print("Some related keywords are: " + ' '.join(synonyms))
    else:
        print("No related keywords found for: " + keyword)
    return synonyms


def scrape(keyword, num_tweets, start_date, end_date):    
    # construct the query
    query = keyword + ' since:' + start_date + ' until:' + end_date
    print(query)

    related(keyword)

    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= num_tweets:
            break
        else:
            tweets.append([tweet.content, tweet.date, tweet.user.username, tweet.url])
    return tweets
 
tweets = scrape("dachshund", 10, '2022-09-05', '2022-10-06')

#user inputs what they want
# keyword = input('Enter a keyword: ')
# num_tweets = int(input('How many tweets do you want to scrape? '))
# since = adjustDate(input('Since (yyyy-mm-dd): '))
# until = adjustDate(input('Until (yyyy-mm-dd, this is exclusive): '))
# scrape(keyword, num_tweets, since, until)

df = pd.DataFrame(tweets, columns=['content', 'date', 'username', 'URL'])
df.to_csv()
print(df) #data could be visualized better


#Example output:

# dachshund since:2022-09-05 until:2022-10-06
# Some related keywords are: dachsie badger_dog
#                                              content  ...                                                URL    
# 0  A dog is now available for adoption! This male...  ...  https://twitter.com/TehamaAnimals/status/15778...    
# 1  Vintage Elegant Porcelain Ceramic Dachshund by...  ...  https://twitter.com/VINTAGE4MOMS/status/157780...    
# 2  @dachshund_heave "Now will you finally play wi...  ...  https://twitter.com/CarnivalOwner/status/15778...    
# 3  @JoeSilverman7 Someone explain the Dachshund r...  ...  https://twitter.com/colonial_bot/status/157780...    
# 4         Dachshund?  How... https://t.co/0UBUCVJK0k  ...  https://twitter.com/surveytheland/status/15778...    
# 5        @dachshund_heave Or separation anxiety 🐈‍⬛🥰  ...  https://twitter.com/45Gigi24/status/157 7808281...
# 6  Check out this listing I just added to my #Pos...  ...  https://twitter.com/rose09estrella/status/1577...    
# 7                @dachshund_heave I forgive you!!! 🥺  ...  https://twitter.com/Oliverbacon247/statu s/1577...
# 8                      @Acyn https://t.co/lN2riJV4w7  ...  https://twitter.com/Freckles3229263/status/157...    
# 9                    @dachshund_heave OMG! STOP IT !  ...  https://twitter.com/F_I_Tally/status/157780649...    

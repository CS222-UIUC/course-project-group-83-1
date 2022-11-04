import re
from nltk.stem.snowball import SnowballStemmer
import spacy


def cleanTweets(text):
    nlp = spacy.load("en_core_web_sm")

    text = regex(text).lower().split()

    # stem words to roots
    stemmer = SnowballStemmer(language="english")
    stems = []
    for word in text:
        stems.append(stemmer.stem(word))

    # remove stopwords
    ret = []
    for word in stems:
        if word not in nlp.Defaults.stop_words:
            ret.append(word)

    return ret


def regex(text):
    text = re.sub("'", "", text)  # keep contractions

    text = re.sub("@[A-Za-z0-9_]+", "", text)  # remove @mentions
    text = re.sub("#", "", text)  # remove #hashtags

    text = re.sub(r"https\S+", "", text)  # remove urls
    text = re.sub(r"www.\S+", "", text)

    text = re.sub("[^A-Za-z0-9]", " ", text)  # remove non-alphanumeric chars

    text = re.sub(r"\s+", " ", text)  # remove extra whitespace

    return text

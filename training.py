import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from spacy.tokens import DocBin

df_pos = pd.read_csv('processedPositive.csv').T.reset_index()
df_neg = pd.read_csv('processedNegative.csv').T.reset_index()
df_neu = pd.read_csv('processedNeutral.csv').T.reset_index()

df_pos['Sentiments'] = 1
df_neg['Sentiments'] = -1
df_neu['Sentiments'] = 0

df = pd.concat([df_pos, df_neg, df_neu], axis=0, ignore_index=True)
df.columns = ['Tweets', 'Sentiments']

# format data for spacy
data = {}
for i, (text, sentiment) in enumerate(zip(df['Tweets'], df['Sentiments'])):
    if sentiment == 1:
        data[i] = {'text': text, 'label': {'pos': 1, 'neg': 0, 'neu': 0}}
    elif sentiment == -1:
        data[i] = {'text': text, 'label': {'pos': 0, 'neg': 1, 'neu': 0}}
    else:
        data[i] = {'text': text, 'label': {'pos': 0, 'neg': 0, 'neu': 1}}

data = list(data.values())
train, test = train_test_split(data, train_size=0.1)

nlp = spacy.blank("en")


def convert(data, output_path):
    # convert data to binary objects
    db = DocBin()
    for line in data:
        doc = nlp.make_doc(line['text'])
        doc.cats = line['label']
        db.add(doc)
    db.to_disk(output_path)


convert(train, "corpus/train.spacy")
convert(test, "corpus/dev.spacy")

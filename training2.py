import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from spacy.tokens import DocBin

df1 = pd.read_json('processed_df_voterfraud.json')
df1.drop(columns=['Date', 'User', 'Subjectivity'], inplace=True)

df2 = pd.read_json('processed_df_election.json')
df2.drop(columns=['Date', 'User', 'Subjectivity'], inplace=True)

df3 = pd.read_json('processed_df_abortion.json')
df3.drop(columns=['Date', 'User', 'Subjectivity'], inplace=True)

df = pd.concat([df1, df2, df3], ignore_index=True)

data = {}
for i, (text, sentiment) in enumerate(zip(df['Tweet'], df['Polarity'])):
    if sentiment >= .1:
        data[i] = {'text': text, 'label': {'pos': 1, 'neg': 0, 'neu': 0}}
    elif sentiment <= -.1:
        data[i] = {'text': text, 'label': {'pos': 0, 'neg': 1, 'neu': 0}}
    else:
        data[i] = {'text': text, 'label': {'pos': 0, 'neg': 0, 'neu': 1}}

data = list(data.values())
train, test = train_test_split(data, train_size=0.1)

nlp = spacy.blank("en")


def convert(data, output_path):
    db = DocBin()
    for line in data:
        doc = nlp.make_doc(line['text'])
        doc.cats = line['label']
        db.add(doc)
    db.to_disk(output_path)


convert(train, "corpus/train.spacy")
convert(test, "corpus/dev.spacy")

# the following installations are required
# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')                   

def analyze_line(nlp_, text):
    doc = nlp_(text)
    pol = doc._.blob.polarity                            # Polarity: -0.125
    sub = doc._.blob.subjectivity                        # Subjectivity: 0.9
    ass = doc._.blob.sentiment_assessments.assessments   # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    grams = doc._.blob.ngrams()   
    result = f"text:{text},pol:{pol},sub:{sub}"
    print(result) 

text = 'loan forgiveness SUCKS i HATE forgiving people EW'
text2 = 'loan forgiveness ROCKS i LOVE forgiving people YAY'
test(nlp,text)
test(nlp,text2)

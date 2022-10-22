# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy, time
from spacytextblob.spacytextblob import SpacyTextBlob

import pandas as pd
import json
from pandas import json_normalize
import numpy as np

import atexit

pol_list = []
sub_list = []

def exit_handler():
    print("Dumping lists")
    with open("backup_list.json", "w") as f:
        f.write(json.dumps([pol_list,sub_list]))
        

atexit.register(exit_handler)


def analyze_line(nlp_, text):
    doc = nlp_(text)
    pol = doc._.blob.polarity                         
    sub = doc._.blob.subjectivity                        
    # ass = doc._.blob.sentiment_assessments.assessments   # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    # grams = doc._.blob.ngrams()   
    return pol, sub

def return_dataframe(json_file):
    df = pd.read_json(json_file)
    #print(df)
    return df

#json_f = "tweets.json"
#return_dataframe(json_f)

def process_data(df, tags): # tags ==> [tweet_col, polarity_col, subjectivity_col]
    tweet_col, pol_col, sub_col = tags
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob') 
    
    progress = 0
    for index, tweet in df[tweet_col].items():
        polarity, subjectivity = analyze_line(nlp, tweet)
        pol_list.append(polarity)
        sub_list.append(subjectivity)
        progress += 1
        if (progress % 10 == 0):
            print(progress)
    df[pol_col] = pol_list
    df[sub_col] = sub_list
    

    return df

def main(json_input, tags, output):
    if (json_input == "" or output == ""):
        raise ValueError("Input/ output file not valid")
    print("Start processing")
    start = time.time()

    df = return_dataframe(json_input)
    
    processed_df = process_data(df, tags)
    print(processed_df)
    with open(output,"w") as f:
        f.write(processed_df.to_json())
    end = time.time()
    
    print("Processing successful")
    print(f"Time taken: {end-start} seconds")
    
tags = ["Tweet", "Polarity", "Subjectivity"]
json_in = "tweets.json"
out_file = "processed_df.json"
main(json_in, tags,out_file)

        

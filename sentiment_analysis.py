# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy, time
from spacytextblob.spacytextblob import SpacyTextBlob

import pandas as pd
import json
from pandas import json_normalize
import numpy as np
import atexit

# Lists holding the tweets' polarity and subjectivity
pol_list = []
sub_list = []

"""
Handles interrupts. Dumps the polarity and subjectivity lists into a back up json file.
    input:
        void
    output:
        void  
"""
def exit_handler():
    print("Dumping lists")
    with open("backup_list.json", "w") as f:
        f.write(json.dumps([pol_list,sub_list]))
        
atexit.register(exit_handler)

"""
Determines the polarity and subjectivity of a single tweet
    input:
        [Language] nlp_ -> spacy Language object with loaded pipeline
        [str] text      -> text to be analyzed
    output:
        [int] pol       -> polarity of text
        [int] sub       -> subjectivity of text
"""
def analyze_line(nlp_, text):
    doc = nlp_(text)
    pol = doc._.blob.polarity                         
    sub = doc._.blob.subjectivity                        
    # ass = doc._.blob.sentiment_assessments.assessments   # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    # grams = doc._.blob.ngrams()   
    return pol, sub

"""
Reads json file of a dataframe and extracts it
    input:
        [str] json_file    -> path to json file, stores the json of a dataframe
    output:
        [Dataframe] df     -> pd.DataFrame object
"""
def return_dataframe(json_file):
    df = pd.read_json(json_file)
    #print(df)
    return df


"""
Appends a polarity and subjectivity column to the given Tweets dataframe
    input:
        [Dataframe] df     -> dataframe of tweets + dates
        [list] tags        -> list of strings, ordered: [tweet_col, polarity_col, subjectivity_col]
    output:
        [Dataframe] df     -> pd.DataFrame object with calculated polarities + subjectivity
"""
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
    
    
def average_polarity(df, tags):
    pol_col, day_col = tags
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob') 
    
    day_total = 0   # total polarity for the day
    day_count = 0   # total recorded polarities for the day

    day_average = []
    day = []

    curr_day = df[day_col][0].floor('d')
    for index, row in df.iterrows():
        if (curr_day != row[day_col].floor('d')):
            print(type(curr_day))
            day.append(curr_day)
            day_average.append(day_total/ day_count)

            day_total = 0
            day_count = 0
            curr_day = row[day_col].floor('d')
        day_total += row[pol_col]
        day_count += 1
        
    if (day_count != 0):
        day.append(curr_day)
        day_average.append(day_total/ day_count)

    df = pd.DataFrame(list(zip(day, day_average)),
               columns =['Date', 'Polarity_Average'])

    return df


def main(json_input, tags, output, avg_output=""):
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
    avg = average_polarity(processed_df,["Polarity","Date"])
    
    print(avg)
    if (avg_output != ""):
        with open(avg_output, "w") as f:
            f.write(avg.to_json())

    print("Average Successful")
    
tags = ["Tweet", "Polarity", "Subjectivity"]
json_in = "tweets.json"
out_file = "processed_df.json"
main(json_in, tags,out_file,"average.json")

        

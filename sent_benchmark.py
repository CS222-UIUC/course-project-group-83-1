# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy, time
from spacytextblob.spacytextblob import SpacyTextBlob

import pandas as pd
import json
from pandas import json_normalize




def analyze_line(nlp_, text,date):
    doc = nlp_(text)
    pol = doc._.blob.polarity                            # Polarity: -0.125
    sub = doc._.blob.subjectivity                        # Subjectivity: 0.9
    # ass = doc._.blob.sentiment_assessments.assessments   # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    # grams = doc._.blob.ngrams()   
    result = f'{date};"{text}";{pol};{sub}'
    return result, pol

def main_(file_input, file_output):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob') 
    
    text = ""
    with open(file_input, "r") as f:
        text = f.read()
    if (text == ""):
        raise ValueError("Input file not valid")
    df = pd.Dataframe(json.loads(text))

    neg = 0
    pos = 0
    neutral = 0
    with open(file_output,"a") as f:
        for index, row in df.iterrows():
            processed, pol = analyze_line(nlp, row["Text"], row["Date"])
            file_output.write(processed + "\n")
            if (pol > .01):
                pos += 1
            elif (pol < -.01):
                neg += 1
            else: 
                neutral += 1
    print(f"negative count: {neg}\npositive count: {pos}\nneutral count: {neutral}")

    
    


        

def create_test_file(file, num_lines):
    text = 'loan forgiveness SUCKS i HATE forgiving people EW'
    text2 = 'loan forgiveness ROCKS i LOVE forgiving people YAY'
    sample = [text,text2]
    c = 0
    with open(file,"w") as f:
        for i in range(0, num_lines):
            f.write(sample[c] + "\n")
            c += 1
            if (c == len(sample)):
                c = 0




def benchmark(file, input, runs): # file -> output file ; input -> input file
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob') 
       
    for i in range(runs):
        start = time.time()
        with open(input,"r") as f:
            for line in f.readlines():
                text = line.strip()
                analyze_line(nlp, text)
        end = time.time()
        time_diff = str(end-start) + " seconds\n"
        with open(file, "a") as f:
            f.write(time_diff)
        print("runs finised:", i)
        
#create_test_file("text_100lines.txt", 100)

benchmark("benchmark_100lines.txt","text_100lines.txt", 20)


# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy, time
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


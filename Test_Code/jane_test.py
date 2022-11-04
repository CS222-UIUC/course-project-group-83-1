import sentiment_analysis as sent
import spacy, time
from spacytextblob.spacytextblob import SpacyTextBlob

import pandas as pd
import json
from pandas import json_normalize
import numpy as np
import atexit

def test_exit():
    try:
        sent.exit_handler()
    except:
        assert False

def test_analyze():
    positive = "I love everything is great happy bright"
    negative = "I hate everything sad angry mad"
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob') 
    try:
        pos_pol, pos_sub = sent.analyze_line(nlp, positive)
        neg_pol, neg_sub = sent.analyze_line(nlp, negative)
        assert pos_pol > 0
        assert neg_pol < 0
    except:
        assert False

def test_dataframe():
    dataframe_file = "dataframe_test.json"
    try:
        df = sent.return_dataframe(dataframe_file)
        assert isinstance(df, pd.DataFrame)
    except:
        assert False

def test_process():
    dataframe_file = "dataframe_test.json"
    try:
        df = sent.return_dataframe(dataframe_file)
        tags = ["Tweet", "Polarity", "Subjectivity"]
        new_df = sent.process_data(df, tags)
        assert isinstance(df, pd.DataFrame)
        assert isinstance(new_df[tags[1]], pd.Series)
        assert isinstance(new_df[tags[2]], pd.Series)
    except:
        assert False

def test_all():
    print("Starting Tests")
    test_exit()
    test_analyze()
    test_dataframe()
    test_process()
    print("All Tests Passed")
test_all()

import pandas as pd
import numpy as np
import json
from pandas import json_normalize
import sentiment_analysis as sent
import matplotlib.pyplot as plt

def plot_pd(pd_json_file):
    df = pd.read_json(pd_json_file)
    #print(df)
    df.plot(x="Date", y="Polarity_Average") # averaged data
    #df.plot(x="Date", y="Polarity") # processed data
    plt.show()
    return df

f = "Average_Data/average_2020_election_week.json.json"
#f = "Processed_Data/processed_2020_election_week.json.json"
plot_pd(f)
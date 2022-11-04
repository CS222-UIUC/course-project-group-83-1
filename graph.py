import pandas as pd
import matplotlib.pyplot as plt

'''
Notes for future: May need to change
graph output fomat (currently
writes to a PNG image)
depending on how the user interface is made.
Also may need to optimize later.
'''

'''
Creates a bar graph of the sentiments
(Positive, Negative, Neutral). This function will
write the graph to an image, named
bar_graph.png
'''

def create_bar(df):
    categories = ["Positive", "Neutral", "Negative"]
    bar_colors = ["tab:green", "tab:grey", "tab:red"]
    #may need to change bounds for categories later
    counts = [df[df["Polarity"] > .10].shape[0], df[(df["Polarity"] >= -.10) & (df["Polarity"] <= .10)].shape[0],
                df[df["Polarity"] < -.10].shape[0]]
    df1 = pd.DataFrame({'Sentiment':categories, 'Counts':counts})
    df1.plot.bar(x = 'Sentiment', y = 'Counts', color = bar_colors, legend=False)
    plt.ylabel("Counts")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("bar_graph.png")

'''
Creates a pie chart of the sentiments
(Positive, Negative, Neutral). Includes percentages.
This function will write the graph to an image,
named pie_chart.png
'''

def create_pie(df):
    categories = ["Positive", "Neutral", "Negative"]
    pie_colors = ["tab:green", "tab:grey", "tab:red"]
    #may need to change bounds for categories later
    counts = [df[df["Polarity"] > .10].shape[0], df[(df["Polarity"] >= -.10) & (df["Polarity"] <= .10)].shape[0],
                df[df["Polarity"] < -.10].shape[0]]
    df2 = pd.DataFrame({'Sentiment':categories, 'Counts':counts})
    df2.plot.pie(y='Counts', autopct='%1.1f%%', labels = categories, colors = pie_colors, legend=False)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("pie_chart.png")

'''
Creates a scatterplot of the total number
of negative, positive, and neutral (represented by
different colors) tweets vs the date by turing a JSON
file into a data frame. This function will
write the graph to an image, named scatter_plot.png
Note: Currently, this function groups the time that
the data was collected in by day, so it is good for
large datasets that span multiple days, but not
good for small datasets that only cover one or a
few days.
'''

def create_scatter(df):
    df['date_no_time'] = df['Date'].dt.normalize()
    unique_dates = df['date_no_time'].unique()
    count_per_category = dict()
    count_per_category["Positive"] = []
    count_per_category["Neutral"] = []
    count_per_category["Negative"] = []
    for i in range(unique_dates.shape[0]):
        df_by_date = df[df['date_no_time'] == unique_dates[i]]
        #may need to change bounds for categories later
        count_per_category["Positive"].append(df_by_date[df_by_date["Polarity"] > .10].shape[0])
        count_per_category["Neutral"].append(df_by_date[(df_by_date["Polarity"] >= -.10) & (df_by_date["Polarity"] <= 10)].shape[0])
        count_per_category["Negative"].append(df_by_date[df_by_date["Polarity"] < -.10].shape[0])
    plt.scatter(unique_dates, count_per_category["Positive"], s =10, c = 'tab:green')
    plt.scatter(unique_dates, count_per_category["Neutral"], s =10, c = 'tab:gray')
    plt.scatter(unique_dates, count_per_category["Negative"], s =10, c = 'tab:red')
    plt.xticks(rotation=20)
    plt.legend(["Positive", "Neutral", "Negative"])
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.savefig("scatter_plot.png")

'''
One function that creates a bar graph, pie chart,
and scatterplot. May save on processing time over
running each function individually since the JSON
is only being converted once, especially once the
JSON file becomes large.
'''

def visualize_data(json_file):
    plt.clf()
    df = pd.DataFrame()
    with open(json_file, 'r') as f:
        df = pd.read_json(f)
    create_scatter(df)
    create_bar(df)
    create_pie(df)

visualize_data("processed_df_abortion.json")

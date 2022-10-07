import pandas as pd
import matplotlib.pyplot as plt

#creates bar graph of sentiments
categories = ["Positive", "Neutral", "Negative"]
counts = [50, 10, 13]
df = pd.DataFrame({'Sentiment':categories, 'Counts':counts})
df.plot.bar(x = 'Sentiment', y = 'Counts')
#plt.show()

#creates pie chart from sentiments
plot = df.plot.pie(y='Counts', figsize=(8, 8))
plt.show()
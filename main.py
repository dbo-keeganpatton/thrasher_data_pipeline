import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

# This is aggregated sentiment scores grouped by interview...
data = pd.read_csv('./data/interview_sentiments.csv')

plt.figure(figsize=(10, 6))

hit_plot = sns.histplot(
    data=data, 
    x='sentiment',
    kde=True,
    bins=30,
    color='skyblue'
)

plt.title('Thrasher Interview Sentiment Distribution', fontsize=16, weight='bold')
plt.xlabel('Sentiment; (+) Positive, (-) Negative', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine()

plt.savefig('./images/SentimentHistogram.png', dpi=300)

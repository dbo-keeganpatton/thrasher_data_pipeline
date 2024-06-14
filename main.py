import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

# This is aggregated sentiment scores grouped by interview...
data = pd.read_csv('./data/interview_sentiments.csv')

plt.figure(figsize=(10, 6))
sns.histplot(data=data, x='sentiment')
plt.title('Thrasher Interview Sentiment Distribution')
plt.xlabel('Sentiment; (+) Positive, (-) Negative')
plt.savefig('test.png')

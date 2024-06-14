import pandas as pd 

# Data 
pd.set_option('display.max_columns', 500)
df = pd.read_csv('./data/processed_data.csv')

grouped_df = df.groupby('title')[['question_processed', 'answer_processed']].mean().reset_index()
grouped_df['sentiment'] = grouped_df['question_processed'] + grouped_df['answer_processed'] / 2

grouped_df.to_csv('./data/interview_sentiments.csv')
 

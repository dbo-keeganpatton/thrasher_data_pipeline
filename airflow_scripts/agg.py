import pandas as pd 
pd.set_option('display.max_columns', 500)



def summarize_sentiment():
    
    df = pd.read_csv('/home/eyelady/projects/python_projects/thrasher_site/data/processed_data.csv')

    grouped_df = df.groupby('title')[['question_processed', 'answer_processed']].mean().reset_index()
    grouped_df['sentiment'] = grouped_df['question_processed'] + grouped_df['answer_processed'] / 2

    return grouped_df.to_csv('/home/eyelady/projects/python_projects/thrasher_site/data/interview_sentiments.csv')
 

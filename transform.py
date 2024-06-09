import pandas as pd
import re
pd.set_option('display.max_columns', 500)


df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)


# I did not address the html tags that made it through'
# Extraction... this is to resolve that.
remove_tags = re.compile('<.*?>')
def clean_title(text):
    text = re.sub(remove_tags, "", text)
    text = re.sub(r'\\', "", text)
   
    return text


df['title'] = df['title'].apply(clean_title)


# dtypes mapping
dtype_dict = {
    'title' : str,
    'question' : str,
    'answer' : str
}

df = df.astype(dtype=dtype_dict)

# There are escape chars throughout the text...
# Just need to get rid of those...
def remove_escape(text):
    text = text.replace('\n', '')
    return text


df['question'] = df['question'].apply(remove_escape)
df['answer'] = df['answer'].apply(remove_escape)


# Stage for ORM
df.to_csv('./data/cleaned_data.csv')

import json
import pandas as pd
from sqlalchemy import create_engine
from nlp import pre_process_text, get_sentiment 
pd.set_option('display.max_columns', 500)


########################
# Database Connections #
########################

with open('./secrets/db_creds.json', 'r') as file:
    secret = json.load(file)


USERNAME = secret["username"]
PASSWORD = secret["password"]
DATABASE = secret["database"]

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost/{DATABASE}")
conn = engine.connect()



########################
#    Data Processing   #
########################

df = pd.read_sql('select * from clean', engine)

# Just filtering out stop words here...
# Then using nltk to assign a polarity score as {column_name}_processed...
for i in df.columns:
    df[i] = df[i].apply(pre_process_text)

for i in df.columns:
    df[f'{i}_processed'] = df[i].apply(get_sentiment)


df.to_csv('./data/processed_data.csv', index=False)

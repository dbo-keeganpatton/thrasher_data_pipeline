import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import json


df = pd.read_csv('./data/cleaned_data.csv')

# Credential Management
with open('./secrets/db_creds.json', 'r') as file:
    secret = json.load(file)


USERNAME = secret["username"]
PASSWORD = secret["password"]
DATABASE = secret["database"]


engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost/{DATABASE}")
meta_data = MetaData()


interview_table = Table(
    'interviews',
    meta_data,
    autoload_with=engine,
    autoload=True
)



with engine.connect() as conn:
    
    for index, row in df.iterrows():
        ins = interview_table.insert().values(
            title=row['title'],
            question=row['question'],
            answer=row['answer']) 
        
        conn.execute(ins)

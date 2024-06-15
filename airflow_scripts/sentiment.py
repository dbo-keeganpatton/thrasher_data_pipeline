import json
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/')
sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/airflow_scripts/utils/')
from nlp import get_sentiment, pre_process_text


pd.set_option('display.max_columns', 500)


def create_sentiment():
    ########################
    # Database Connections #
    ########################

    with open('/home/eyelady/projects/python_projects/thrasher_site/secrets/db_creds.json', 'r') as file:
        secret = json.load(file)


    USERNAME = secret["username"]
    PASSWORD = secret["password"]
    DATABASE = secret["database"]

    engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost/{DATABASE}")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    query = 'select * from clean'
    result = session.execute(query)
    rows = result.fetchall()
    columns = result.keys()

    df = pd.DataFrame(rows, columns=columns)
    session.close()


    ########################
    #    Data Processing   #
    ########################

    # Just filtering out stop words here...
    # Then using nltk to assign a polarity score as {column_name}_processed...
    for i in df.columns:
        df[i] = df[i].apply(pre_process_text)

    for i in df.columns:
        df[f'{i}_processed'] = df[i].apply(get_sentiment)


    return df.to_csv('/home/eyelady/projects/python_projects/thrasher_site/data/processed_data.csv', index=False)

if __name__ == "__main__":
    create_sentiment()

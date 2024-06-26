import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import json
import sys
import os

sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/')


def load_func():
    df = pd.read_csv('/home/eyelady/projects/python_projects/thrasher_site/data/cleaned_data.csv')

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
    )


    Session = sessionmaker(bind=engine)
    session = Session()



    try:    
        
        for index, row in df.iterrows():
            
            ins = interview_table.insert().values(
                title=row['title'],
                question=row['question'],
                answer=row['answer']) 
        
            session.execute(ins)
            
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

    finally:
        session.close()
    
    
    try:
        if os.path.exists('/home/eyelady/projects/python_projects/thrasher_site/data/cleaned_data.csv'):
            os.remove('/home/eyelady/projects/python_projects/thrasher_site/data/cleaned_data.csv')
    
    except FileNotFoundError as e:
        print(f'{e}')
        pass

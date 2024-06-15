from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import declarative_base
import json 
import sys

sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/')


def create_func():
# Credential Management
    with open('./secrets/db_creds.json', 'r') as file:
        secret = json.load(file)
        

    USERNAME = secret["username"]
    PASSWORD = secret["password"]
    DATABASE = secret["database"]


    engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost/{DATABASE}")
    engine.connect()
    Base = declarative_base()


    class interviews(Base):
        __tablename__ = 'interviews'
        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String)
        question = Column(String)
        answer = Column(String)



    inspector = inspect(engine)
    if 'interviews' not in inspector.get_table_names():
        Base.metadata.create_all(engine) 


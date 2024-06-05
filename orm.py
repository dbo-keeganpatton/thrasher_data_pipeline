from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
import json 

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

    proName = Column(String, primary_key=True)
    question = Column(String)
    answer = Column(String)



Base.metadata.create_all(engine) 


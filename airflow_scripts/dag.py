# Repo loc
import sys
sys.path.append('/home/eyelady/projects/python_projects/thrasher_site/airflow_scripts/')

# DAG step dependecies
from transform import transform_func 
from orm import create_func
from load import load_func
from sentiment import create_sentiment
from agg import summarize_sentiment

# Airflow 
from airflow.models import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import os 


#############
#   Files   #
#############

file_location = '/home/eyelady/projects/python_projects/thrasher_site/airflow_scripts/'
site_utils = os.path.join(file_location, 'site_utils')
extract_file = os.path.join(file_location, 'scrape.py')


###########
#   DAG   #
###########

args = {
    'owner' : 'airflow',
    'start_date' : datetime(2024, 6, 9),
    'retries' : 2,
    'retry_delay' : timedelta(seconds=10)
}

dag = DAG(
    dag_id='thrasher_article_pipeline',
    default_args=args,
    schedule_interval=timedelta(weeks=1)
)


###########
#  Tasks  #
###########

@task(task_id='Extract', dag=dag)
def extract():
    exec(open( extract_file ).read())

@task(task_id='Transform', dag=dag)
def transform():
    transform_func()

@task(task_id='Create', dag=dag)
def create_table():
    create_func()

@task(task_id='Load', dag=dag)
def load():
    load_func()

@task.bash
def dbt_run():
    return "pwd && cd ${AIRFLOW_HOME} && cd projects/python_projects/thrasher_site/interviews/ && dbt run"

@task(task_id='sentiment', dag=dag)
def sentiment():
    create_sentiment()

@task(task_id='summarize', dag=dag)
def agg_sentiment():
    summarize_sentiment()


############
#   Flow   #
############
extract() >> transform() >> create_table() >> load() >> dbt_run() >> sentiment() >> agg_sentiment()

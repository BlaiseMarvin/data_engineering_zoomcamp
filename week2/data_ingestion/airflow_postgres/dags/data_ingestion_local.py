from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from ingest_script import main
import os

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME","/opt/airflow/")
URL ="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz"

# we could dynamically have our URL download a particular file each year and month using this Jinja templating as shown below
# URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz"
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'

PG_HOST= os.environ.get("PG_HOST")
PG_USER=os.environ.get("PG_USER")  
PG_PASSWORD=os.environ.get("PG_PASSWORD")  
PG_PORT= os.environ.get("PG_PORT")
PG_DATABASE=os.environ.get("PG_DATABASE")

local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 1-12 *",
    start_date=days_ago(2),
    catchup=False
)

with local_workflow:
    wget_task = BashOperator(
        task_id="extract",
        bash_command=f'curl -L {URL} | gunzip > {OUTPUT_FILE_TEMPLATE}'
        # ds is a string whereas execution_date is a datetime object - we now format the datetime object
        # to extract the year and month as below
        # bash_command = 'echo ""'
    )

    ingest_task=PythonOperator(
        task_id='ingest',
        python_callable=main,
        op_kwargs=dict(
            user=PG_USER, 
            password=PG_PASSWORD, 
            host=PG_HOST, 
            port=PG_PORT, 
            db=PG_DATABASE, 
            table_name="yellow_trips", 
            csv_file=OUTPUT_FILE_TEMPLATE
        )
    )

    wget_task >> ingest_task
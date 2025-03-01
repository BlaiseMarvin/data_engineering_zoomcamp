from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from ingest_script import yellow_insertion
import os

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME","/opt/airflow/")

yellow_trips_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz"
green_trips_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz"

OUTPUT_FILE_TEMPLATE1 = AIRFLOW_HOME + '/output_yellow_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
OUTPUT_FILE_TEMPLATE2 = AIRFLOW_HOME + '/output_green_{{ execution_date.strftime(\'%Y-%m\') }}.csv'

PG_USER = 'postgres'
PG_PASSWORD = 'supersecret'
PG_DATABASE = 'ny_taxi'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

postgres_ingest_dag = DAG("postgres_ingestion", start_date=datetime(2021,1,1),default_args=default_args,end_date=datetime(2021,7,31),catchup=True, schedule_interval="0 0 5 1-12 *")

with postgres_ingest_dag:
    # download the yellow trips data
    extract_yellow_data = BashOperator(
        task_id = "extract_yellow_data",
        bash_command = f"curl -L {yellow_trips_url} | gunzip > {OUTPUT_FILE_TEMPLATE1}"
    )

    # green trips data extraction
    extract_green_data = BashOperator(
        task_id="extract_green_data",
        bash_command = f"curl -L {green_trips_url} | gunzip > {OUTPUT_FILE_TEMPLATE2}"
    )

    ingest_yellow_task = PythonOperator(
        task_id='ingest_yellow',
        python_callable=yellow_insertion,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host="database",
            db = PG_DATABASE,
            port="5432",
            table_name="yellow_trips",
            csv_file="output_yellow_{{ execution_date.strftime(\'%Y-%m\') }}.csv"
        )
    
    )
    


    extract_yellow_data >> ingest_yellow_task


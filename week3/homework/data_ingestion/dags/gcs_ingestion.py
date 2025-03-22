import os
import logging
import urllib.request
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME","/opt/airflow/")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BIGQUERY_DATASET = "yellowtrips_jan2june"

def upload_to_gcs(bucket,object_name,local_file):
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# DAG declaration 
with DAG(
    dag_id = "data_ingestion_gcs_dag",
    schedule_interval=None,
    default_args=default_args,
    catchup=False
) as dag:
    for i in [f"0{i}" for i in range(1,7)]:
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{i}.parquet"

        download_task = BashOperator(
            task_id = f"download_task_{i}",
            bash_command=f"curl -L {url} > {AIRFLOW_HOME}/yellow_tripdata_2024-{i}.parquet"
        )

        local_to_gcs = PythonOperator(
            task_id = f"local_to_gcs_{i}",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": f"raw/yellow_tripdata_2024-{i}.parquet",
                "local_file": f"{AIRFLOW_HOME}/yellow_tripdata_2024-{i}.parquet"
            }
        )
        download_task.set_downstream(local_to_gcs)
        # download_task >> local_to_gcs

with DAG(
    dag_id="external_bq_table",
    schedule_interval=None,
    default_args=default_args,
    catchup=False
) as dag2:
    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [
                    f"gs://{BUCKET}/raw/yellow_tripdata_2024-*.parquet"
                ],
            },
        },
    )
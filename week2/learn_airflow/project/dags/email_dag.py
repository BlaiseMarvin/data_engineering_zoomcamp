try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators import EmailOperator
    from datetime import datetime

    # setting up triggers
    from airflow.utils.trigger_rule import TriggerRule
    import airflow.hooks.S3_hook

    print("All Dag modules are ok ........ ")
except Exception as e:
    print("Error {}".format(e))

def first_function(**context):
    print("Hello world this works ")

def on_failure_callback(context):
    print("Fail works ! ")


with DAG(
    dag_id="email_dag",
    schedule_interval="@once",
    default_args={
        "owner":"airflow",
        "start_date": datetime(2020,11,1),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": on_failure_callback,
        "email": ['jackreacher@gmail.com'],
        "email_on_failure": False,
        "email_on_retry": False
    },
    catchup=False
) as dag:
    first_function = PythonOperator(
        task_id = "first_function",
        python_callable=first_function
    )

    email = EmailOperator(
        task_id="send_email",
        to="",
        subject="Airflow Alert",
        html_content=""" <h3> Email Test Airflow </h3>"""
    )

    first_function >> email
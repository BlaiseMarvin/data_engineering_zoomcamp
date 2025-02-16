try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    print("All Dag Modules are ok........")
except Exception as e:
    print("Error {} ".format(e))


def first_function_execute(**kwargs):
    print("First function Execute ")
    variable = kwargs.get("name","Didn't get the name")
    print("Hello World: Mr. {}".format(variable))
    return "Hello World " + variable

# 
# def second_function_execute(*args,**kwargs):

# for the schedule interval -> it is also possible to provide your crontab expression such as
# */2 **** Execute every 2 minutes

with DAG(
    dag_id = "first_dag",
    schedule_interval="@daily",
    default_args={
        "owner":"airflow",
        "retries":1,
        "retry_delay":timedelta(minutes=5),
        "start_date": datetime(2021,2,16)
    },
    catchup=False
) as f:
    first_function_execute = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute,
        op_kwargs={"name":"Blaise Rusoke"}
    )
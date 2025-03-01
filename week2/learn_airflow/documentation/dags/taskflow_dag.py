# this tutorial builds on the regular airflow tutorial and focuses on writing data pipelines using the 
# TaskFlow API paradigm which is introduced as part of airflow 2.0 and contrasts this with DAGs written using the
# traditional paradigm
# example: TaskFlow API Pipeline
import json
import pendulum
from airflow.decorators import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021,1,1,tz="UTC"),
    catchup=False,
    tags=["example"],
)
def tutorial_taskflow_api():
    """
        ### TaskFlow API Tutorial Documentation
        This is a simple data pipeline example which demonstrates the use of
        the TaskFlow API using 3 simple tasks for Extract, Transform, and Load.
        Documentation that foes along with the Airflow TaskFlow API tutorial is
    """
    @task()
    def extract():
        """
            #### Extract Task
            A simple extract task to get data ready for the rest of the data pipeline
            In this case, getting data is simulated by reading from a hardcoded JSON string
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict
    
    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
            Transform task
            A simple transform task - takes in the collection of order data and 
            computes the total order value
        """
        total_order_value = 0

        for value in 

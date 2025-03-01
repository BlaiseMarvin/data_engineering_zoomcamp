FROM apache/airflow:2.2.3

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER 0


USER $AIRFLOW_UID

WORKDIR $AIRFLOW_HOME
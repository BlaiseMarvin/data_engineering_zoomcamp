FROM python:3.9

RUN apt-get install wget

RUN apt-get install curl

RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python","ingest_data.py" ]
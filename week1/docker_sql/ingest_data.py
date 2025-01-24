import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    out2 = 'output.csv.gz'
    csv_name = 'output.csv'

    # download the csv file
    os.system(f"wget {url} -O {out2}")
    os.system(f"gunzip {out2}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    # get the next object out of the iterator
    df = next(df_iter)

    # convert these datetime columns to time
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # use the head = 0 to insert only the head - create the table at this point

    df.head(n=0).to_sql(con=engine, name=table_name, if_exists='replace')

    # so that worked, now we need to insert the entire batch:
    df.to_sql(con=engine,name=table_name,if_exists='append')

    # Iterators will always work when the next function is called till there isn't any more data to insert. 
    # we utilise this and keep on inserting more data. 


    while True:
        t_start = time()
        df_ = next(df_iter)

        df_.tpep_pickup_datetime = pd.to_datetime(df_.tpep_pickup_datetime)
        df_.tpep_dropoff_datetime = pd.to_datetime(df_.tpep_dropoff_datetime)

        df_.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print(f'inserted another chunk....., took {round(t_end-t_start,3)} seconds')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ingest CSV Data to Postgres')

    # arguments: user, password, host, port , db name, table_name, url

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)

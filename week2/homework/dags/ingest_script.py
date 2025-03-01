import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

def yellow_insertion(user,password,host,port,db,table_name,csv_file):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    df_iter = pd.read_csv(csv_file,iterator=True,chunksize=100000)

    df = next(df_iter)

    # # convert these datetime columns to time
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # we only do this, if we are reading the first batch of data from 2021 January
    if csv_file=="output_yellow_2021-01.csv":
        df.head(n=0).to_sql(con=engine, name=table_name, if_exists='replace')
    
    df.to_sql(con=engine,name=table_name,if_exists='append')

    z = None

    while True:
        chunk = next(df_iter, None)
        if type(chunk) != type(z):
            # process data
            chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
            chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
            # insert the chunk
            chunk.to_sql(con=engine, name=table_name, if_exists='append')
        else:
            break
        



import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

def main(user, password, host, port, db, table_name, csv_file):
    print(table_name, csv_file)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    
    # # get the next object out of the iterator
    df = next(df_iter)

    # # convert these datetime columns to time
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # # use the head = 0 to insert only the head - create the table at this point

    df.head(n=0).to_sql(con=engine, name=table_name, if_exists='replace')

    # # so that worked, now we need to insert the entire batch:
    df.to_sql(con=engine,name=table_name,if_exists='append')

    # # Iterators will always work when the next function is called till there isn't any more data to insert. 
    # # we utilise this and keep on inserting more data. 
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
    # while True:
    #     t_start = time()
    #     df_ = next(df_iter)

    #     df_.tpep_pickup_datetime = pd.to_datetime(df_.tpep_pickup_datetime)
    #     df_.tpep_dropoff_datetime = pd.to_datetime(df_.tpep_dropoff_datetime)

    #     df_.to_sql(name=table_name, con=engine, if_exists='append')
    #     t_end = time()
    #     print(f'inserted another chunk....., took {round(t_end-t_start,3)} seconds')




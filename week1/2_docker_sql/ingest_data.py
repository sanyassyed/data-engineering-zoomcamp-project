#!/usr/bin/env python
# coding: utf-8

# # Code to load data from CSV to a DB on Postgres using Python

import pandas as pd
import os
# package to connect to the DB
from sqlalchemy import create_engine
import argparse
import wget

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    # ## Setting Up Database Connection
    # connecting to postgres and to the ny_taxi DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # ## Batching the Dataset

    # to process only the first 100 rows
    # df = pd.read_csv(FULL_PATH, nrows=100)

    # Processing the dataset in batches
    if csv_name.endswith('.csv.gz'):
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, low_memory=False, compression='gzip') #nrows=200000,
    else:
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, low_memory=False)


    # iterating through the batches of data
    df = next(df_iter)


    # Changing the datatype of the datetime colums recording pickup and dropoff time
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    # ## Inserting table header only

    # Extracting only the table header to use it for table definition in the DB and then insert only that into the table yellow_taxi_data
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')


    # ## Inserting first data chunk into the table

    # Inserting data rows into the DB into the table yellow_taxi_data
    df.to_sql(name=table_name, con=engine, if_exists='append')


    # ## Inserting subsequent data chunks into the table using a loop

    from time import time
    loop = True
    while loop:
        t_start = time()
        
        # trying to catch the error thrown when the iterator becomes empty
        try:
            df = next(df_iter)
        except StopIteration:
            loop = False
            print("Iteration is stopped")
            break
        
        # Changing the datatype of the datetime colums recording pickup and dropoff time
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        
        print(f'Finished inserting chunk in {(t_end-t_start):.3f} seconds')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database_name name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--url', help='url for csv data')

    args = parser.parse_args()
    
    main(args)

# python -m wget "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz" -O "output.csv"
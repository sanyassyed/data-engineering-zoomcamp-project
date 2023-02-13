#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta
import pyarrow as pa


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url:str) -> pd.DataFrame:
    """Reads the dataset from the URL into pandas DF"""
    if 'fhv_tripdata_2020-01' in dataset_url:
        df=pd.read_csv(dataset_url, encoding='latin1')
    # causes error for fhv file 2020 Jan so removed pyarrow
    else:
        df=pd.read_csv(dataset_url, encoding='latin1', engine='pyarrow')
    return df

@task(log_prints=True)
def clean_fhv(df:pd.DataFrame) -> pd.DataFrame:
    """Fix some dtype issues"""
    # fixing column names
    df.columns = ['dispatching_base_num', 'pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID', 'SR_Flag', 'Affiliated_base_number']
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], unit ='ns')
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], unit ='ns')
    # Change the dtypes setting so int values can be 0
    df = df.convert_dtypes()
    # define datatypes of other columns
    df = df.astype({'dispatching_base_num': 'string', 
                'PULocationID': 'Int64',
                'DOLocationID': 'Int64',
                'SR_Flag': 'Int64',
                'Affiliated_base_number': 'string'})
    return df     

@task(log_prints=True)
def clean_color(df:pd.DataFrame, color:str) -> pd.DataFrame:
    """Fix some dtype issues"""
    if color == 'yellow':
        col_names = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
    else:
        col_names = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    df[col_names[0]] = pd.to_datetime(df[col_names[0]], unit ='ns')
    df[col_names[1]] = pd.to_datetime(df[col_names[1]], unit ='ns')
    # Change the dtypes setting so int values can be 0
    df = df.convert_dtypes()
    # defining the schema
    df = df.astype({ 'VendorID': 'int64', 
                'passenger_count': 'int64',
                'trip_distance': 'float64',
                'RatecodeID': 'int64',
                'store_and_fwd_flag':'bool',
                'PULocationID': 'int64',
                'DOLocationID': 'int64',
                'payment_type': 'int64',
                'fare_amount': 'float64',
                'extra': 'float64',
                'mta_tax': 'float64',
                'tip_amount': 'float64',
                'tolls_amount': 'float64',
                'improvement_surcharge': 'float64',
                'total_amount': 'float64',
                'congestion_surcharge': 'float64'}, errors='ignore')
    return df  

@task(retries=3)
def write_local(df: pd.DataFrame, dataset_file:str, ftype:str, taxi_cat:str) -> Path:
    # make output directory if it does not exist
    data_fol = 'parq' if ftype == 'parquet' else ftype
    output_dir = Path(f'data/{data_fol}/{taxi_cat}')
    output_dir.mkdir(parents=True, exist_ok=True)
    path = Path(f"{output_dir}/{dataset_file}.{ftype}.gz")
    df.to_parquet(path, compression="gzip", engine='pyarrow')
    return path


@task(retries=3)
def write_to_gcs(path:Path) -> None:
    """Loads the dataset into GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    return 

@flow(name='SubSubFlowLogging', log_prints=True)
def log_sub_subflow(row_number:int, month:int, year:int, datatypes:dict, path:Path) -> None:
    """Logs the number of rows in the dataset being writted to GCS"""
    print(f'Logging the number of rows in the dataset for the month {month} in the year {year}: {row_number}')
    print(f'Logging Dtypes of df = {datatypes}')
    print(f'Logging data storage path: {path}')
    return

@flow(name='SubFlowIngest')
def etl_subflow(month:int, year:int, ftype:str, taxi_cat:str) -> None:
    """Sub Flow performing main EL"""

    dataset_file = f'{taxi_cat}_tripdata_{year}-{month:02}'
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_cat}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    if taxi_cat == 'fhv':
        df = clean_fhv(df)
    else:
        df = clean_color(df, taxi_cat)
    path = write_local(df, dataset_file, ftype, taxi_cat)
    row_number = df.shape[0]
    log_sub_subflow(row_number, month, year, (df.dtypes).to_dict(), path)
    write_to_gcs(path)

@flow(name='ParentFlow')
def etl_parent_flow(months:list[int]=[1], years:list[int]=[2019, 2020], ftypes:list[int]=[1,2], categories:list[int]=[1,2,3]) -> None:
    """The Parent flow that calls the sub flow to perform ETL for each month"""
    # file storage format on GCS
    ftype_dict = {1:'csv', 2: 'parquet'}
    # taxi data category
    taxi_cat_dict = {1: 'green', 2:'yellow', 3:'fhv'}
    for ftype in ftypes:
        for taxi_cat in categories:
            for year in years:
                for month in months:
                    etl_subflow(month, year, ftype_dict[ftype], taxi_cat_dict[taxi_cat])

if __name__=="__main__":
    """Accepts years in list, 
    month number in list, 
    file formats- 1 for csv, 2 for parquet, 
    taxi types - 1 for green, 2 for yellow, 3 for fhv"""
    # months the data is required for
    months = [1]
    # years the data is required for
    years = [2020]
    ftypes = [2]
    categories = [3]
    etl_parent_flow(months, years, ftypes, categories)

# Q1
# Start prefect orion `prefect orion start`
# Set the config for the api `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`
# Then run this file from the week_2_workflow_orchestration folder as `python .\etl_web_to_gcs.py`

# Write file locally as gzip and count the number of rows to cross check
# wget "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz" -O "tes.csv.gz"
#`gzip -d -c .\tes.csv.gz | wc -l`

# Q2
# Option 1 - Schedule via command line
# Build & Schedule & Apply in 1 step
# `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL" --cron "0 5 1 * *" --timezone "UTC" -a`

# Option 2 - Schedule via UI
# Build and Apply - use this if you want add parameters after build to the .yaml file
# `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL"`
# `prefect deployment apply etl_parent_flow-deployment.yaml`

# Q3
# Parameters to use to load data to GCS
# "color": "yellow", "months" :[2,3], "year": 2019

# EDA Useful functions in Pandas
# df.shape
# df.info()
# df.describe(include='all').T
# df.dtypes

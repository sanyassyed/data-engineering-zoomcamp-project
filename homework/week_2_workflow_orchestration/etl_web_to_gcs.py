#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url:str) -> pd.DataFrame:
    """Reads the dataset from the URL into pandas DF"""
    df=pd.read_csv(dataset_url, low_memory=False)
    return df

@task(log_prints=True)
def clean(df:pd.DataFrame, color:str) -> pd.DataFrame:
    """Fix some dtype issues"""
    if color == 'yellow':
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    else:
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    return df

@task(retries=3)
def write_local(df: pd.DataFrame, dataset_file:str, color:str) -> Path:
    # make output directory if it does not exist
    output_dir = Path(f'data/{color}')
    output_dir.mkdir(parents=True, exist_ok=True)
    path = Path(f"{output_dir}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task(retries=3)
def write_to_gcs(path:Path) -> None:
    """Loads the dataset into GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    return 

@flow(name='SubSubFlowLogging', log_prints=True)
def log_sub_subflow(row_number:int) -> None:
    """Logs the number of rows in the dataset beign writted to GCS"""
    print(f'Logging the number of rows in the dataset: {row_number}')
    return

@flow(name='SubFlowIngest')
def etl_subflow(color:str, month:int, year:int) -> None:
    """Sub Flow performing main EL"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df = clean(df, color)
    path = write_local(df, dataset_file, color)
    row_number = df.shape[0]
    log_sub_subflow(row_number)
    write_to_gcs(path)

@flow(name='ParentFlow')
def etl_parent_flow(color:str='green', months:list[int]=[6], year:int=2020) -> None:
    """The Parent flow that calls the sub flow to perform ETL for each month"""
    for month in months:
        etl_subflow(color, month, year)

if __name__=="__main__":
    color = 'green'
    months = [7]
    year = 2020
    etl_parent_flow(color, months, year)

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



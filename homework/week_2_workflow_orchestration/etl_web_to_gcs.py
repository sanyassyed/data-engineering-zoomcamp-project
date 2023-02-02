#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task(retries=3)
def fetch(dataset_url:str) -> pd.DataFrame:
    """Reads the dataset from the URL into pandas DF"""
    df=pd.read_csv(dataset_url, low_memory=False)
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

@flow(name='SubFlow', log_prints=True)
def log_subflow(row_number:int) -> None:
    print(f'Logging the number of rows in the dataset: {row_number}')
    return

@flow(name='IngestFlow')
def etl_web_to_gcs(color:str, month:int, year:int) -> None:
    """Main EL Flow"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    path = write_local(df, dataset_file, color)
    row_number = df.shape[0]
    log_subflow(row_number)
    write_to_gcs(path)


if __name__=="__main__":
    color = 'green'
    month = 1
    year = 2020
    etl_web_to_gcs(color, month, year)

# Q1
# Start prefect orion `prefect orion start`
# Set the config for the api `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`
# Then run this file from the week_2_workflow_orchestration folder as `python .\etl_web_to_gcs.py`

# Write file locally as gzip and count the number of rows to cross check
# wget "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz" -O "tes.csv.gz"
#`gzip -d -c .\tes.csv.gz | wc -l`

# Q2
# Build and Deploy

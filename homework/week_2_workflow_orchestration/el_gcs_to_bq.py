#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color:str, month:int, year:int) -> Path:
    """Download trip data from GCS"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}.parquet'
    data_dir = f'data'
    gcs_path = f"{data_dir}/{color}/{dataset_file}"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f".")
    return Path(gcs_path).as_posix()


@task(retries=3)
def write_to_bq(path:Path) -> int:
    """Loads the dataset as Dataframe and writes it into BQ"""
    df = pd.read_parquet(path)
    gcp_credentials_block = GcpCredentials.load('google-credentials')
    df.to_gbq(destination_table = 'trips_data_all.rides_hw', project_id='blissful-flames-375219', credentials=gcp_credentials_block.get_credentials_from_service_account(), chunksize=500000, if_exists='append')
    return df.shape[0]

@flow(name='SubFlowLogging', log_prints=True)
def log_subflow(table_rows:int, total_rows:int, i:int) -> None:
    """Logs the number of rows in the dataset beign writted to BQ"""
    print(f'Logging: Dataset {i} - number of rows written to BQ: {table_rows}')
    print(f'Logging: Total Number of rows from all datasets written until now: {total_rows}')


@flow(name='SubFlowIngest')
def el_subflow(color:str, month:int, year:int) -> None:
    """Sub Flow performing main EL"""
    path = extract_from_gcs(color, month, year)
    row_count = write_to_bq(path)
    return row_count

@flow(name='ParentFlow')
def el_parent_flow(color:str='green', months:list[int]=[1,2], year:int=2021) -> None:
    """The Parent flow that calls the sub flow to perform EL for each month"""
    total_rows = 0
    for i, month in enumerate(months):
        table_rows = el_subflow(color, month, year)
        total_rows += table_rows
        log_subflow(table_rows, total_rows, i)

if __name__=="__main__":
    color = 'green'
    months = [1]
    year = 2020
    el_parent_flow(color, months, year)

# Q3
# Parameters to use to load data to GCS
# "color": "yellow", "months" :[2,3], "year": 2019
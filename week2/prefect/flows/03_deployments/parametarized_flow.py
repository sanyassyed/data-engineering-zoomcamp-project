#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta
import os

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url:str) -> pd.DataFrame:
    """Read taxi data from web  into pandas Dataframe"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df:pd.DataFrame) -> pd.DataFrame:
    """Fix some dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    #print(df.head(2))
    #print(f'columns: {df.dtypes}')
    #print(f'rows: {len(df)}')
    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    # make output directory if it does not exist
    output_dir = Path(f'data/{color}')
    output_dir.mkdir(parents=True, exist_ok=True)
    # print(f"Current working directory is: {os.getcwd()}")
    path = Path(f"{output_dir}/{dataset_file}.parquet")
    # print(f"Path for data is: {path}")
    df.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path):
    """Uploading local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix())
    return


@flow()
def etl_web_to_gcs(year:int, month:int, color:str) -> None:
    """The main ETL function"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)

@flow()
def etl_parent_flow(months: list[int] = [1,2], year:int = 2021, color:str = 'yellow') -> None:
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__== '__main__':
    color = 'yellow'
    months = [1]
    year =2021
    etl_parent_flow(months, year, color)

# Type 1: Parametarized from CLI 
# Use the command :python .\flows\03_deployments\parametarized_flow.py

# Type 2 : Build and apply deployment so we can schedule this code and run via the agent.
# Step 1: Build the Deployment
# prefect deployment build .\flows\03_deployments\parametarized_flow.py:etl_parent_flow -n "Parameterized ETL" -o "./flows/03_deployments/etl_parent_flow-deployment"
# This will create a yaml file and you can pass the parameters there too
# Step 2: Apply the deployment by typing
# prefect deployment apply .\flows\03_deployments\etl_parent_flow-deployment.yaml
# Then go to the UI and Add Description/Scheduling/Run the deployment
# Then turn on the agent so it can pickup the deployment from the queue named 'default'
# parameters for yml file
#  "color": "yellow", "months" :[4,5], "year": 2021
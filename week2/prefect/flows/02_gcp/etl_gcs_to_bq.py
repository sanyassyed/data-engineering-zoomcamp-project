#!/usr/bin/env python
# coding: utf-8
from pathlib  import Path
import pandas as p
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color:str, year:int, month:int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f'data/{color}/{color}_tripdata_{year}-{month:02}.parquet'
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f".")
    return Path(gcs_path)
   
@task()
def transform(path:Path) -> p.DataFrame:
    """Data cleaning example: Fill NA value in passenger_count column with 0"""
    df = p.read_parquet(path)
    print(f"pre:missing passenger count from the df: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post:missing passenger count from the df: {df['passenger_count'].isna().sum()}")
    return df

@task(retries=3)
def write_bq(df:p.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load('google-credentials')
    df.to_gbq(destination_table='trips_data_all.rides', project_id='blissful-flames-375219', credentials=gcp_credentials_block.get_credentials_from_service_account(), chunksize=500000, if_exists='append')


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load datat into Big Query"""
    color = 'yellow'
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    #print(f'GCS path is: {path}')
    df = transform(path)
    write_bq(df)
    


if __name__=='__main__':
    etl_gcs_to_bq()


# Run the file from the `prefect` folder where the data folder resides
# python /flows/02_gcp/etl_gcs_to_bq.py

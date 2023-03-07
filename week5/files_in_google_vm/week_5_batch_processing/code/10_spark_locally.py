#!/usr/bin/env python
# coding: utf-8

# In[1]:

import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os


parser = argparse.ArgumentParser()

parser.add_argument('--input_green', required=True)
parser.add_argument('--input_yellow', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input_green = args.input_green
input_yellow = args.input_yellow
output = args.output

'''
# Method 1: where you specify one master inside the code
spark = SparkSession.builder\
                    .master("spark://de-zoomcamp.us-central1-c.c.blissful-flames-375219.internal:7077")\
                    .appName('test')\
                    .getOrCreate()
'''

# Method 2: where you specify the master outside the code
spark = SparkSession.builder\
                    .appName('test')\
                    .getOrCreate()

# Adding all green taxi data for 2020 and 2021 to one PySpark DF
# Path: Stop at the root folder that contains all the parts of one file
# Eg: The root folder data/green/2021/01 contains all the partitions for the month on January which is one file
df_green = spark.read.parquet(input_green)

# Adding all yellow taxi data for 2020 and 2021 to one PySpark DF

df_yellow = spark.read.parquet(input_yellow)

# The pickup_datetime column is missing so will rename those columns in both the datasets
df_green = df_green \
                    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
                    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')
df_yellow = df_yellow\
                     .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
                     .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')        


# Extracting common columns
#we will check if the column in green trip data is available in yellow trip data and then append it to a list
common_columns = [x for x in df_green.columns if x in set(df_yellow.columns)]
print(common_columns)

# saving the common columns for future use to specify the schema
common_columns = [
     'VendorID',
     'pickup_datetime',
     'dropoff_datetime',
     'store_and_fwd_flag',
     'RatecodeID',
     'PULocationID',
     'DOLocationID',
     'passenger_count',
     'trip_distance',
     'fare_amount',
     'extra',
     'mta_tax',
     'tip_amount',
     'tolls_amount',
     'improvement_surcharge',
     'total_amount',
     'payment_type',
     'congestion_surcharge']


# Select these common columns from the datset and assign to a new dataset
# select() function is similar to the select clause in SQL
df_green_sel = df_green \
                        .select(common_columns) \
                        .withColumn('service_type', F.lit('green'))

# select() function is similar to the select clause in SQL
df_yellow_sel = df_yellow \
                        .select(common_columns) \
                        .withColumn('service_type', F.lit('yellow'))


# Combine the two datasets
df_trips_data = df_green_sel.unionAll(df_yellow_sel)

df_trips_data.registerTempTable('trips_data')

df_result = spark.sql("""
SELECT 
    -- Reveneue grouping 
    PULocationID as revenue_zone,
    date_trunc('month', pickup_datetime) as revenue_month, 
    service_type, 
    -- Revenue calculation 
    SUM(fare_amount) as revenue_monthly_fare,
    SUM(extra) as revenue_monthly_extra,
    SUM(mta_tax) as revenue_monthly_mta_tax,
    SUM(tip_amount) as revenue_monthly_tip_amount,
    SUM(tolls_amount) as revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) as revenue_monthly_improvement_surcharge,
    SUM(total_amount) as revenue_monthly_total_amount,
    SUM(congestion_surcharge) as revenue_monthly_congestion_surcharge,

    -- Additional calculations
    avg(passenger_count) as avg_montly_passenger_count,
    avg(trip_distance) as avg_montly_trip_distance

FROM 
    trips_data
GROUP BY 
    1,2,3;
""")


# writing the data to the local machine
# to set the partitioning to 215
# df_result = df_result.repartition(215)


# to change the partitioning to 1 use coalesce
df_result.coalesce(1).write.parquet(output, mode='overwrite')

print('Completed writing report to the local system')

'''
Notes:
# Method 1: when we specify spark master cluster url inside the code
# run from this folder: week_5_batch_processing the following code to execute this file
python code/10_spark_locally.py \
    --input_green=data/pq/green/2020/* \
    --input_yellow=data/pq/yellow/2020/* \
    --output=data/report-2020
'''

'''
# Method 2: when we specify spark master cluster outside using spark-submit script
# Specify the spark master URL outside the code

URL="spark://de-zoomcamp.us-central1-c.c.blissful-flames-375219.internal:7077"

spark-submit \
    --master="${URL}" \
    code/10_spark_locally.py \
        --input_green=data/pq/green/2021/* \
        --input_yellow=data/pq/yellow/2021/* \
        --output=data/report-2021
'''


'''
# Method-2: 
# Sub Method 1: Via DataProc UI
# Dataproc commands
# copy this file to GCS
gsutil cp 10_spark_locally.py gs://dtc_data_lake_blissful-flames-375219/code/10_spark_locally.py

# Arguments
--input_green=gs://dtc_data_lake_blissful-flames-375219/pq/green/2021/* \
--input_yellow=gs://dtc_data_lake_blissful-flames-375219/pq/yellow/2021/* \
--output=gs://dtc_data_lake_blissful-flames-375219/report-2021

# Sub Method 2: Via DataProc CLI
# copy this file to GCS
gsutil cp 10_spark_locally.py gs://dtc_data_lake_blissful-flames-375219/code/11_spark__bq.py
# Execute the command in data_proc.sh by copy pasting the code in command line
'''
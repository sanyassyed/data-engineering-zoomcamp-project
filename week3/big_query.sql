-- Counting rows in the rides table
SELECT COUNT(*) FROM `blissful-flames-375219.trips_data_all.rides`;

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `blissful-flames-375219.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_blissful-flames-375219/data/yellow/yellow_tripdata_2019-*.csv.gz', 'gs://dtc_data_lake_blissful-flames-375219/data/yellow/yellow_tripdata_2020-*.csv.gz']
);

-- Check yelllow trip data
SELECT * FROM `blissful-flames-375219.trips_data_all.external_yellow_tripdata` LIMIT 10;

-- Create NON-parititioned table from external table by omiting the index column and converting vendor column to type int
CREATE OR REPLACE TABLE `blissful-flames-375219.trips_data_all.yellow_tripdata_non_partitoned` AS
SELECT CAST(VendorID AS int64) AS VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, CAST(passenger_count AS int64) as passenger_count, trip_distance, CAST(RatecodeID as int64) as RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, CAST(payment_type as int64) as payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge FROM `blissful-flames-375219.trips_data_all.external_yellow_tripdata`;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE `blissful-flames-375219.trips_data_all.yellow_tripdata_partitoned`
PARTITION BY
  DATE(tpep_pickup_datetime) AS 
SELECT CAST(VendorID AS int64) AS VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, CAST(passenger_count AS int64) as passenger_count, trip_distance, CAST(RatecodeID as int64) as RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, CAST(payment_type as int64) as payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge FROM `blissful-flames-375219.trips_data_all.external_yellow_tripdata`; 

-- Impact of partition
-- Scanning 1.65GB of data
SELECT DISTINCT(VendorID)
FROM `blissful-flames-375219.trips_data_all.yellow_tripdata_non_partitoned`
WHERE DATE (tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM `blissful-flames-375219.trips_data_all.yellow_tripdata_partitoned`
WHERE DATE (tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Lets look into the partitions
SELECT table_name, partition_id, total_rows
FROM `trips_data_all.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name='yellow_tripdata_partitoned'
ORDER BY total_rows DESC;


-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `blissful-flames-375219.trips_data_all.yellow_tripdata_partitoned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT CAST(VendorID AS int64) AS VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, CAST(passenger_count AS int64) as passenger_count, trip_distance, CAST(RatecodeID as int64) as RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, CAST(payment_type as int64) as payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge FROM `blissful-flames-375219.trips_data_all.external_yellow_tripdata`;


-- Query scans 1.1 GB
SELECT count(*) as trips
FROM `blissful-flames-375219.trips_data_all.yellow_tripdata_partitoned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM `blissful-flames-375219.trips_data_all.yellow_tripdata_partitoned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
AND VendorID=1;
-- Initial setup
-- Created a new dataset called `tripdata_hw` with the same region as the project

-- Creating external table
CREATE OR REPLACE EXTERNAL TABLE `blissful-flames-375219.tripdata_hw.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_blissful-flames-375219/data_hw/tripdata_2019-*.csv.gz']
);

-- Create a BQ table from the external table
CREATE OR REPLACE TABLE  `blissful-flames-375219.tripdata_hw.fhv_tripdata` AS
SELECT * FROM `blissful-flames-375219.tripdata_hw.external_fhv_tripdata`;

-- Q1 What is the count for fhv vehicle records for year 2019?
SELECT COUNT(*) FROM `blissful-flames-375219.tripdata_hw.fhv_tripdata`;
-- Answer: 43244696

-- Question 2:
-- Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.</br> 
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT DISTINCT(Affiliated_base_number) FROM `blissful-flames-375219.tripdata_hw.external_fhv_tripdata`;
SELECT DISTINCT(Affiliated_base_number) FROM `blissful-flames-375219.tripdata_hw.fhv_tripdata`;
-- Answer: - 0 MB for the External Table and 317.94MB for the BQ Table 


-- Question 3:
-- How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT COUNT(1) FROM `blissful-flames-375219.tripdata_hw.fhv_tripdata`
WHERE PULocationID IS NULL AND
DOLocationID IS NULL;
-- Answer:717,748

-- Question 4
-- What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
-- Answer: Partition by pickup_datetime Cluster on affiliated_base_number

-- Question 5
--Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31. Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

-- partition & cluster
CREATE OR REPLACE TABLE `blissful-flames-375219.tripdata_hw.fhv_tripdata_partitioned_clustered` 
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM `blissful-flames-375219.tripdata_hw.external_fhv_tripdata`;

-- Select distinct affiliated base number from fhv_tripdata_partitioned_clustered table
SELECT DISTINCT(Affiliated_base_number) 
FROM `blissful-flames-375219.tripdata_hw.fhv_tripdata_partitioned_clustered`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31'; 
-- 23.05

-- Select distinct affiliated base number from fhv_tripdata table
SELECT DISTINCT(Affiliated_base_number) 
FROM `blissful-flames-375219.tripdata_hw.fhv_tripdata`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

--Answer: 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table

-- Question 6 
-- Where is the data stored in the External Table you created?
-- Answer: GCP Bucket

-- Question 7:
-- It is best practice in Big Query to always cluster your data:
-- Answer: False

-- Parquet
-- Initial setup

-- Creating external table
CREATE OR REPLACE EXTERNAL TABLE `blissful-flames-375219.tripdata_hw.external_ft_parquet` 
(dispatching_base_num	STRING, 
pickup_datetime	TIMESTAMP, 
dropoff_datetime	TIMESTAMP, 
PULocationID INT64, 
DOLocationID	INT64, 
SR_Flag	INT64,		
Affiliated_base_number	STRING)
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_blissful-flames-375219/data_hw_parquet/tripdata_2019-*.parquet',
  'gs://dtc_data_lake_blissful-flames-375219/data_hw_parquet/tripdata_2020-*.parquet']
);

-- specifying datatypes for columns
-- (dispatching_base_num	STRING, pickup_datetime	TIMESTAMP, dropoff_datetime	TIMESTAMP, PULocationID FLOAT64, DOLocationID	FLOAT64, SR_Flag	INT64,		Affiliated_base_number	STRING)
-- Create a table from the external table
CREATE OR REPLACE TABLE  `blissful-flames-375219.tripdata_hw.ft_parquet` AS
SELECT * FROM `blissful-flames-375219.tripdata_hw.external_ft_parquet`;
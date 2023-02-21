-- production dataset
--Q1
SELECT COUNT(*) FROM `blissful-flames-375219.production.fact_trips` 
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2020-12-31';
--61648442 (order by fare_amount, PULocationid, tpep_pickup_datetime, tpep_dropoff_datetime in green and yellow staging models)

--Q3
SELECT COUNT(*) FROM `blissful-flames-375219.production.stg_fhv_tripdata`
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2019-12-31';
-- 43244696 (with no where clause)
-- 43244693 (with where clause)

--Q4
SELECT COUNT(*) FROM `blissful-flames-375219.production.fact_fhv_trips` 
WHERE DATE(pickup_datetime) BETWEEN '2019-01-01' AND '2019-12-31';
--22998722 (same answer with and without the where clause in stg_fhv_tripdata model)

-- Link to report on Looker Studio:
-- https://lookerstudio.google.com/s/tOiJl_aoyp0

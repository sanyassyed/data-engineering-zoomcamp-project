--Modify the ingest_data.py file to accept the different column names
--Rebuild the Docker Image taxi_ingest:v001 that ingests the data
--Start PostgresDB and Pgadmin using docker-compose
--Run the image  and set the Url and table name differently before executing the command to populate the DB

--Question 3. Count records 
--How many taxi trips were totally made on January 15?
SELECT
	COUNT(1)
FROM
	green_taxi_trips t 
WHERE 
CAST("lpep_pickup_datetime" as date) = '2019-01-15'::date AND
CAST("lpep_dropoff_datetime" as date) = '2019-01-15'::date
--*Answer: 20530*

--Question 4. Largest trip for each day
--Which was the day with the largest trip distance (Use the pick up time for your calculations.)?
--Soln 1
SELECT
	CAST("lpep_pickup_datetime" as date) d,
	trip_distance as dist
FROM
	green_taxi_trips t 
ORDER BY dist DESC

--Soln 2
SELECT "lpep_pickup_datetime"::date as "Day with Max Trip Distance" 
FROM green_taxi_trips
WHERE "trip_distance" = (SELECT MAX("trip_distance") FROM green_taxi_trips t )

--*Answer: 2019-01-15*

--Question 5. The number of passengers
--In 2019-01-01 how many trips had 2 and 3 passengers?
--Soln 1:
SELECT 
	"passenger_count" as pc,
	COUNT(1)
FROM green_taxi_trips
WHERE "lpep_pickup_datetime"::date = '2019-01-01' AND "passenger_count" IN (2,3)
GROUP BY pc

--Soln 2
SELECT CAST("lpep_pickup_datetime" as date) "pickup_date",
		"passenger_count" as "total_passengers",
		COUNT(2)
FROM 
	green_taxi_trips g
WHERE
	"passenger_count" IN (2,3) AND
	CAST("lpep_pickup_datetime" as date) = '2019-01-01'::date
GROUP BY 
	"pickup_date", "total_passengers"
ORDER BY
	"total_passengers"

--*Answer: - 2: 1282 ; 3: 254*

--Question 6. Largest tip
-- For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? (We want the name of the zone, not the id.)

SELECT 
	z2."Zone" as "dropoff_zone",
	g."DOLocationID" "dropoff_zone_id",
	g."tip_amount" "tip",	
	z1."Zone" as "pickup_zone",
	g."PULocationID" "pickup_zone_id"
FROM 
	green_taxi_trips g,
	zones z1,
	zones z2
WHERE
	g."PULocationID" = z1."LocationID" AND
	g."DOLocationID" = z2."LocationID" AND
	z1."Zone" = 'Astoria'
ORDER BY
	tip DESC
LIMIT 1

--*Answer: Long Island City/Queens Plaza*


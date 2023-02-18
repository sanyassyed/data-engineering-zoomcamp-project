
with tripdata as
(
 select *,
 row_number() over(partition by VendorID, lpep_pickup_datetime) as rn
 from `blissful-flames-375219`.`trips_data_all`.`green_tripdata`
where VendorID is not null
)
select 
-- identifiers
    to_hex(md5(cast(coalesce(cast(VendorID as 
    string
), '') || '-' || coalesce(cast(lpep_pickup_datetime as 
    string
), '') as 
    string
))) as tripid,
    cast(VendorID as integer) as vendorid,
    cast(RatecodeID as integer) as ratecodeid,
    cast(PULocationID as INTEGER) as pickup_locationid,			
    cast(DOLocationID as INTEGER) as dropoff_locationid,

    -- timestamps
    cast(lpep_pickup_datetime as TIMESTAMP) as pickup_datetime,			
    cast(lpep_dropoff_datetime as TIMESTAMP) as dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    cast(passenger_count as	INTEGER) as passenger_count,			
    cast(trip_distance as numeric)	as trip_distance,
    cast(trip_type as integer) as trip_type,

    -- payment info	
    cast(fare_amount as numeric) as fare_amount,			
	cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(ehail_fee as integer) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    cast(payment_type as integer) as payment_type,
    

    case payment_type
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end
 as payment_type_description,
    cast(congestion_surcharge as numeric) as congestion_surcharge
from tripdata	
where rn = 1
-- dbt build --m <model.sql> --var 'is_test_run: false'


    limit 100

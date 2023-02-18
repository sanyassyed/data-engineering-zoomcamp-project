

select 
    LocationId as locationid,
    Borough as borough,
    Zone as zone,
    replace(service_zone, 'Boro', 'Green') as service_zone
from `blissful-flames-375219`.`dbt_sanya_models`.`taxi_zone_lookup`
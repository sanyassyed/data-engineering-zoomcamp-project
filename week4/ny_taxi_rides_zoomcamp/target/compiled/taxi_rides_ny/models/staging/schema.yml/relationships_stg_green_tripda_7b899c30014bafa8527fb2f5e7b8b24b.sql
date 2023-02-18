
    
    

with child as (
    select pickup_locationid as from_field
    from `blissful-flames-375219`.`dbt_sanya_models`.`stg_green_tripdata`
    where pickup_locationid is not null
),

parent as (
    select locationid as to_field
    from `blissful-flames-375219`.`dbt_sanya_models`.`taxi_zone_lookup`
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select tripid
from `blissful-flames-375219`.`dbt_sanya_models`.`stg_yellow_tripdata`
where tripid is null



      
    ) dbt_internal_test
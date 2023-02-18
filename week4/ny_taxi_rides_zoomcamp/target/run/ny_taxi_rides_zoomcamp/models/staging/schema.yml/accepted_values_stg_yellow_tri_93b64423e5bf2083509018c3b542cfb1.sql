select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        payment_type as value_field,
        count(*) as n_records

    from `blissful-flames-375219`.`dbt_sanya_models`.`stg_yellow_tripdata`
    group by payment_type

)

select *
from all_values
where value_field not in (
    1,2,3,4,5,6
)



      
    ) dbt_internal_test
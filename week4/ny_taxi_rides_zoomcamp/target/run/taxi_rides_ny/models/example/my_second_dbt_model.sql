

  create or replace view `blissful-flames-375219`.`dbt_sanya_models`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `blissful-flames-375219`.`dbt_sanya_models`.`my_first_dbt_model`
where id = 1;


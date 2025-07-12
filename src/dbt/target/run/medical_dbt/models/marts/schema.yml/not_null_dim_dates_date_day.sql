
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_day
from "medical_insights"."public"."dim_dates"
where date_day is null



  
  
      
    ) dbt_internal_test
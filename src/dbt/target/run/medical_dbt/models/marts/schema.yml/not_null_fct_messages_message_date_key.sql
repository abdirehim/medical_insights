
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_date_key
from "medical_insights"."public"."fct_messages"
where message_date_key is null



  
  
      
    ) dbt_internal_test
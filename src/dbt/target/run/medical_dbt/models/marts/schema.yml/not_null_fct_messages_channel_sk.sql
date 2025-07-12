
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_sk
from "medical_insights"."public"."fct_messages"
where channel_sk is null



  
  
      
    ) dbt_internal_test
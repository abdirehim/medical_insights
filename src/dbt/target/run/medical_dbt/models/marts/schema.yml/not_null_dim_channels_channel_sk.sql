
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_sk
from "medical_insights"."public"."dim_channels"
where channel_sk is null



  
  
      
    ) dbt_internal_test
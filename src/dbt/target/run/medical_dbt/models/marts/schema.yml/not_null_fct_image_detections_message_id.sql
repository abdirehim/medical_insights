
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_id
from "medical_insights"."public"."fct_image_detections"
where message_id is null



  
  
      
    ) dbt_internal_test
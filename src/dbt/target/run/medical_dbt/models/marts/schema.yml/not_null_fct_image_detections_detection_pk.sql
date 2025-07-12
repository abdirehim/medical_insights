
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select detection_pk
from "medical_insights"."public"."fct_image_detections"
where detection_pk is null



  
  
      
    ) dbt_internal_test
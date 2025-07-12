
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select object_class
from "medical_insights"."public"."fct_image_detections"
where object_class is null



  
  
      
    ) dbt_internal_test

    
    

select
    detection_pk as unique_field,
    count(*) as n_records

from "medical_insights"."public"."fct_image_detections"
where detection_pk is not null
group by detection_pk
having count(*) > 1



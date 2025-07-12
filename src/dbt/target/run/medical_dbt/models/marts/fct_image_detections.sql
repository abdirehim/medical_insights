
  create view "medical_insights"."public"."fct_image_detections__dbt_tmp"
    
    
  as (
    -- models/marts/fct_image_detections.sql

SELECT
    md5(concat(message_id::text, object_class, detection_time::text)) AS detection_pk, -- surrogate key
    message_id,
    image_id,
    object_class,
    confidence_score,
    detection_time
FROM (
    VALUES
        (NULL, NULL, NULL, NULL, NULL) -- Placeholder row, to be replaced by enrichment process
) AS t(message_id, image_id, object_class, confidence_score, detection_time)
WHERE message_id IS NOT NULL
  );

    
    

select
    channel_sk as unique_field,
    count(*) as n_records

from "medical_insights"."public"."dim_channels"
where channel_sk is not null
group by channel_sk
having count(*) > 1



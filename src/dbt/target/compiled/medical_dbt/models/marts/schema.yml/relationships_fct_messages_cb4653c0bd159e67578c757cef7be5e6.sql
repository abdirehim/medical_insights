
    
    

with child as (
    select channel_sk as from_field
    from "medical_insights"."public"."fct_messages"
    where channel_sk is not null
),

parent as (
    select channel_sk as to_field
    from "medical_insights"."public"."dim_channels"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



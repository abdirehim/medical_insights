
    
    

with child as (
    select message_date_key as from_field
    from "medical_insights"."public"."fct_messages"
    where message_date_key is not null
),

parent as (
    select date_day as to_field
    from "medical_insights"."public"."dim_dates"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



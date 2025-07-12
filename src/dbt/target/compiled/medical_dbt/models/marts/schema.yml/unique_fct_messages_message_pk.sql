
    
    

select
    message_pk as unique_field,
    count(*) as n_records

from "medical_insights"."public"."fct_messages"
where message_pk is not null
group by message_pk
having count(*) > 1




    
    

select
    id as unique_field,
    count(*) as n_records

from "medical_insights"."public"."stg_telegram_messages"
where id is not null
group by id
having count(*) > 1



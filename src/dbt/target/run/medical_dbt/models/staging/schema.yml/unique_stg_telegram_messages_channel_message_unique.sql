
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    channel_message_unique as unique_field,
    count(*) as n_records

from "medical_insights"."public"."stg_telegram_messages"
where channel_message_unique is not null
group by channel_message_unique
having count(*) > 1



  
  
      
    ) dbt_internal_test
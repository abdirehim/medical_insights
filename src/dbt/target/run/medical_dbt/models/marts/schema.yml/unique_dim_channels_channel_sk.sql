
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    channel_sk as unique_field,
    count(*) as n_records

from "medical_insights"."public"."dim_channels"
where channel_sk is not null
group by channel_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test
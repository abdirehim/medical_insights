-- models/marts/fct_messages.sql

WITH stg_messages AS (
    SELECT
        id,
        channel_name,
        message_id,
        message_text,
        message_date,
        views_count,
        forwards_count,
        replies_count,
        has_reactions,
        has_photo,
        product_mentions,
        scraped_at
    FROM "medical_insights"."public"."stg_telegram_messages"
),

channels AS (
    SELECT
        channel_name,
        channel_sk
    FROM "medical_insights"."public"."dim_channels"
),

dates AS (
    SELECT
        date_day,
        year,
        month,
        day_of_month
    FROM "medical_insights"."public"."dim_dates"
)

SELECT
    sm.id AS message_pk,
    sm.message_id,
    sm.message_text,
    LENGTH(sm.message_text) AS message_length,
    sm.message_date,
    sm.views_count,
    sm.forwards_count,
    sm.replies_count,
    sm.has_reactions,
    sm.has_photo,
    sm.product_mentions,
    sm.scraped_at,
    c.channel_sk,
    d.date_day AS message_date_key
FROM stg_messages sm
LEFT JOIN channels c ON sm.channel_name = c.channel_name
LEFT JOIN dates d ON sm.message_date::DATE = d.date_day
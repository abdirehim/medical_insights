-- models/marts/dim_channels.sql

SELECT DISTINCT
    channel_name,
    MD5(channel_name) AS channel_sk -- Surrogate key for channel
FROM {{ ref('stg_telegram_messages') }}
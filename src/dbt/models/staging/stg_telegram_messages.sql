-- models/staging/stg_telegram_messages.sql

WITH raw_messages AS (
    SELECT
        id,
        channel_name,
        message_id,
        data AS raw_data,
        scraped_at
    FROM {{ source('raw', 'telegram_messages') }}
),

cleaned_messages AS (
    SELECT
        id,
        channel_name,
        message_id,
        scraped_at,
        raw_data->>'message' AS message_text,
        (raw_data->>'date')::TIMESTAMP AS message_date,
        (raw_data->>'views')::INT AS views_count,
        (raw_data->>'forwards')::INT AS forwards_count,
        (raw_data->'replies'->>'replies') AS replies_count, -- Fixed extraction for replies_count
        (raw_data->>'reactions') IS NOT NULL AS has_reactions,
        (raw_data->>'photo') IS NOT NULL AS has_photo,
        -- Extract product mentions (enhanced regex for Ethiopian context)
        REGEXP_MATCHES(
            raw_data->>'message',
            '(?i)(paracetamol|amoxicillin|ibuprofen|diclofenac|metronidazole|coartem|albendazole|ORS|syrup|tablet|capsule|suspension|injection|vaccine|antimalarial|antibiotic|antifungal|antiviral|cream|pill)s?',
            'g'
        ) AS product_mentions,
        channel_name || '-' || message_id AS channel_message_unique
    FROM raw_messages
    WHERE raw_data->>'message' IS NOT NULL OR raw_data->>'photo' IS NOT NULL
),

deduped_messages AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY channel_name, message_id ORDER BY scraped_at ASC) AS rn
    FROM cleaned_messages
)

SELECT
    id,
    channel_name,
    message_id,
    message_text,
    message_date,
    COALESCE(views_count, 0) AS views_count,
    COALESCE(forwards_count, 0) AS forwards_count,
    COALESCE(replies_count::INT, 0) AS replies_count,
    has_reactions,
    has_photo,
    product_mentions,
    scraped_at,
    channel_message_unique
FROM deduped_messages
WHERE rn = 1
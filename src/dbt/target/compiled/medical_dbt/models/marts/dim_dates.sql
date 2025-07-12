-- models/marts/dim_dates.sql

WITH date_spine AS (
    SELECT
        GENERATE_SERIES(
            '2023-01-01'::DATE,
            CURRENT_DATE + INTERVAL '1 year',
            '1 day'::INTERVAL
        )::DATE AS date_day
),

date_attributes AS (
    SELECT
        date_day,
        EXTRACT(YEAR FROM date_day) AS year,
        EXTRACT(MONTH FROM date_day) AS month,
        TO_CHAR(date_day, 'Month') AS month_name,
        EXTRACT(DAY FROM date_day) AS day_of_month,
        EXTRACT(DOW FROM date_day) AS day_of_week, -- Sunday = 0, Saturday = 6
        TO_CHAR(date_day, 'Day') AS day_name,
        EXTRACT(DOY FROM date_day) AS day_of_year,
        EXTRACT(WEEK FROM date_day) AS week_of_year,
        EXTRACT(QUARTER FROM date_day) AS quarter_of_year,
        TO_CHAR(date_day, 'YYYY-MM') AS year_month,
        TO_CHAR(date_day, 'YYYY-MM-DD') AS full_date_string,
        (CASE WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE ELSE FALSE END) AS is_weekend
    FROM date_spine
)

SELECT *
FROM date_attributes
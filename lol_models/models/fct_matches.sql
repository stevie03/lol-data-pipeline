{{config(materialized='table')}}

with daily_stats as (
    SELECT
        DATE(CAST(MATCH_DATE AS TIMESTAMP)) AS match_date,
        COUNT(DISTINCT MATCH_ID) AS matches_played,
        SUM(KILLS) AS total_kills,
        SUM(DEATHS) AS total_deaths,
        SUM(ASSISTS) AS total_assists
        FROM  {{source('match_history', 'matches')}}
        WHERE UPPER(result) != 'REMAKE'
        GROUP BY 1
),
kda_stats as (
    SELECT
        match_date,
        matches_played,
        total_kills,
        total_deaths,
        total_assists,
        (total_kills + total_assists) / NULLIF(total_deaths, 0) AS kda_ratio
    FROM daily_stats
)
 
SELECT
    match_date,
    matches_played,
    total_kills,
    total_deaths,
    total_assists,
    ROUND(kda_ratio, 2) AS kda_ratio,
    ROUND(AVG(kda_ratio) OVER (ORDER BY match_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS kda_7_day_avg
FROM kda_stats
ORDER BY match_date DESC

     

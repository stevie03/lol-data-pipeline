{{config(materialized='table')}}

with raw_data as (
     SELECT * FROM match_history.matches
)


SELECT
    match_id,
    player_name,
    match_date,
    game_mode,
    champion_played,
    kills,
    deaths,
    assists,
    ROUND((kills + assists) / GREATEST(deaths, 1), 2) AS kda,
    damage_dealt,
    gold_earned,
    result,
    match_duration
FROM raw_data

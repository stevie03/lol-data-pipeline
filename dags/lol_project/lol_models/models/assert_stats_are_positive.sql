select
    match_date,
    total_kills,
    total_deaths,
    total_assists
from {{ ref('fct_matches') }}
where total_kills < 0
   or total_deaths < 0
   or total_assists < 0
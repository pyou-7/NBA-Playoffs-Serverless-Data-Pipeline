WITH cte AS (
  SELECT
  game_date,
  team_abbreviation,
  MAX(game_season) AS season,
  SUM(fg3a) AS total_fg3a,
  MAX(team_game_score) AS team_game_score
FROM final_nba_playoffs_data_parquet_tbl_prod
GROUP BY game_date, team_abbreviation
)
SELECT
  AVG(total_fg3a) AS avg_fg3a,
  AVG(team_game_score) AS avg_game_score
FROM cte
GROUP BY season
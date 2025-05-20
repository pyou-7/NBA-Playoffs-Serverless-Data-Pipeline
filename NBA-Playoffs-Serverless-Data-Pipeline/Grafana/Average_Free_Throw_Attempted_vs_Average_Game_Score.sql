WITH cte AS (
  SELECT
  game_date,
  team_abbreviation,
  MAX(game_season) AS season,
  SUM(fta) AS total_fta,
  MAX(team_game_score) AS team_game_score
FROM final_nba_playoffs_data_parquet_tbl_prod
GROUP BY game_date, team_abbreviation
)
SELECT
  AVG(total_fta) AS avg_fta,
  AVG(team_game_score) AS avg_game_score
FROM cte
GROUP BY season
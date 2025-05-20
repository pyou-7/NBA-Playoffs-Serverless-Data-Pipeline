WITH aggregated_score AS (
  SELECT
    team_name, 
    game_date,
    MAX(team_game_score) AS team_score
  FROM final_nba_playoffs_data_parquet_tbl_prod 
  GROUP BY team_name, game_date
)
SELECT
  DATE_TRUNC('year', CAST(game_date AS DATE)) AS time,
  AVG(team_score) AS avg_team_score
FROM aggregated_score
WHERE $__timeFilter(CAST(game_date AS TIMESTAMP))
GROUP BY DATE_TRUNC('year', CAST(game_date AS DATE))
ORDER BY 1
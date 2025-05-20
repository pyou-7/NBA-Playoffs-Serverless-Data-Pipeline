SELECT
  player_name,
  SUM(ast) AS total_assists
FROM final_nba_playoffs_data_parquet_tbl_prod
GROUP BY player_name
ORDER BY total_assists DESC
LIMIT 15

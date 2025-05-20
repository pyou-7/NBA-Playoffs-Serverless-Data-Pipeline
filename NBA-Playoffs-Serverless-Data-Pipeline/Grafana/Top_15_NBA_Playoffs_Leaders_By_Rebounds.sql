SELECT
  player_name,
  SUM(reb) AS total_rebounds
FROM final_nba_playoffs_data_parquet_tbl_prod
GROUP BY player_name
ORDER BY total_rebounds DESC
LIMIT 15

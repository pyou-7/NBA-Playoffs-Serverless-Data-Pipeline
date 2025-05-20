SELECT
  player_name,
  SUM(pts) AS total_points
FROM final_nba_playoffs_data_parquet_tbl_prod
GROUP BY player_name
ORDER BY total_points DESC
LIMIT 15

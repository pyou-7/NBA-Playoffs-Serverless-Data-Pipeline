SELECT
  player_name,
  COUNT(*) AS appearances
FROM final_nba_playoffs_data_parquet_tbl_prod
WHERE min > 0 
GROUP BY player_name
ORDER BY appearances DESC
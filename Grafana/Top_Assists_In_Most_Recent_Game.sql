SELECT
  MAX(ast)
FROM final_nba_playoffs_data_parquet_tbl_prod
WHERE game_date = (SELECT MAX(game_date) FROM final_nba_playoffs_data_parquet_tbl_prod) 
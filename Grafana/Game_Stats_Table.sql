SELECT
  player_name,
  team_name,
  team_conference,
  game_date,
  min,
  pts,
  reb,
  ast,
  stl,
  blk,
  turnover,
  team_game_score
FROM final_nba_playoffs_data_parquet_tbl_prod
WHERE game_date = (SELECT MAX(game_date) FROM final_nba_playoffs_data_parquet_tbl_prod ) 
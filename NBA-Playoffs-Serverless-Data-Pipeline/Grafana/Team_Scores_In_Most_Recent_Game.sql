SELECT
  team_abbreviation,
  team_conference,
  team_game_score
FROM final_nba_playoffs_data_parquet_tbl_prod
WHERE game_date = (SELECT MAX(game_date) FROM final_nba_playoffs_data_parquet_tbl_prod ) 
GROUP BY team_abbreviation, team_conference, team_game_score
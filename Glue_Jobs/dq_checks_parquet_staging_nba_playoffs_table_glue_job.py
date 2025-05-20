import sys
import awswrangler as wr

# this check counts the number of NULL rows in the temp_C column
# if any rows are NULL, the check returns a number > 0
NULL_DQ_CHECK = f"""
SELECT 
    SUM(CASE WHEN player_name IS NULL THEN 1 ELSE 0 END) AS player_null_count,
    SUM(CASE WHEN team_name IS NULL THEN 1 ELSE 0 END) AS team_null_count,
    SUM(CASE WHEN team_conference IS NULL THEN 1 ELSE 0 END) AS conference_null_count,
    SUM(CASE WHEN game_date IS NULL THEN 1 ELSE 0 END) AS date_null_count,
    SUM(CASE WHEN team_game_score IS NULL THEN 1 ELSE 0 END) AS game_score_null_count
FROM "nba-playoffs-proj-db"."staging_nba_playoffs_daily_data_parquet_tbl"
;
"""

# run the quality check
df = wr.athena.read_sql_query(sql=NULL_DQ_CHECK, database="de_proj_database")

# exit if we get a result > 0
# else, the check was successful
if df['player_null_count'][0] > 0 or df['team_null_count'][0] > 0 or df['conference_null_count'][0] > 0 or df['date_null_count'][0] > 0 or df['game_score_null_count'][0] > 0:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')

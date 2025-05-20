import sys
import boto3

client = boto3.client('athena')

SOURCE_TABLE_NAME = 'nba_crawler_nba_playoffs_daily_stats_bucket'
NEW_TABLE_NAME = 'staging_nba_playoffs_daily_data_parquet_tbl'
NEW_TABLE_S3_BUCKET = 's3://nba-playoffs-daily-stats-staging-bucket/'
MY_DATABASE = 'nba-playoffs-proj-db'
QUERY_RESULTS_S3_BUCKET = 's3://query-results-location-nba-playoffs-proj'

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE {NEW_TABLE_NAME} WITH
    (external_location='{NEW_TABLE_S3_BUCKET}',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['yr_partition'])
    AS

    SELECT
        CONCAT("player.first_name", ' ', "player.last_name") AS player_name,
        "player.position" AS player_position,
        "team.full_name" AS team_name,
        "team.abbreviation" AS team_abbreviation,
        "team.conference" AS team_conference,
        "game.date" AS game_date,
        "game.season" AS game_season,
        "min",
        "fgm",
        "fga",
        "fg_pct",
        "fg3m",
        "fg3a",
        "fg3_pct",
        "ftm",
        "fta",
        CAST(NULLIF(CAST("ft_pct" AS VARCHAR), 'nan') AS DOUBLE) AS ft_pct,
        "oreb",
        "dreb",
        "reb",
        "ast",
        "stl",
        "blk",
        "turnover",
        "pf",
        "pts",
        CASE
            WHEN "team.id" = "game.home_team_id" THEN "game.home_team_score"
            WHEN "team.id" = "game.visitor_team_id" THEN "game.visitor_team_score"
        END AS team_game_score,
        SUBSTRING("game.date",1,4) AS yr_partition
    FROM "{MY_DATABASE}"."{SOURCE_TABLE_NAME}"
    WHERE 
    "team.conference" IN ('West', 'East')
    AND
    CAST("game.date" AS timestamp) >= current_timestamp - interval '2' day
    ;
    """,
    
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_S3_BUCKET}'}
)

# list of responses
resp = ["FAILED", "SUCCEEDED", "CANCELLED"]

# get the response
response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])

# wait until query finishes
while response["QueryExecution"]["Status"]["State"] not in resp:
    response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])
    
# if it fails, exit and give the Athena error message in the logs
if response["QueryExecution"]["Status"]["State"] == 'FAILED':
    sys.exit(response["QueryExecution"]["Status"]["StateChangeReason"])
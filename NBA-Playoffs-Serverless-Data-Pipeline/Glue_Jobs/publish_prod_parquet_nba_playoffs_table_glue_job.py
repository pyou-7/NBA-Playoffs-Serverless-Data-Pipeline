import sys
import boto3
from datetime import datetime

QUERY_RESULTS_BUCKET = 's3://query-results-location-nba-playoffs-proj/'
MY_DATABASE = 'nba-playoffs-proj-db'
SOURCE_PARQUET_TABLE_NAME = 'staging_nba_playoffs_daily_data_parquet_tbl'
PROD_PARQUET_TABLE_NAME = 'final_nba_playoffs_data_parquet_tbl_prod'

# create a string with the current UTC datetime
# convert all special characters to underscores
# this will be used in the table name and in the bucket path in S3 where the table is stored
DATETIME_NOW_INT_STR = str(datetime.now()).replace('-', '_').replace(' ', '_').replace(':', '_').replace('.', '_')

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    INSERT INTO {PROD_PARQUET_TABLE_NAME}
    SELECT * FROM {SOURCE_PARQUET_TABLE_NAME}
    ;
    """,
    
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_BUCKET}'}
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

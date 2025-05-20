import boto3
import requests
import pandas as pd
import io
from datetime import datetime

FIREHOSE_NAME = 'PUT-S3-cfoDD'
API_URL = "https://api.balldontlie.io/v1/stats"

def lambda_handler(event, context):
    headers = {
        "Authorization": API_KEY,
        "User-Agent": "Mozilla/5.0"
    }

    today = datetime.now().strftime('%Y-%m-%d')
    params = {
        "dates[]": today,
        "per_page": 100,
        "postseason": "true"
    }

    response = requests.get(API_URL, headers=headers, params=params, timeout=20)
    data = response.json().get("data", [])

    if not data:
        print(f"No NBA playoff stats found for {today}. Nothing will be ingested.")
        return {
            "statusCode": 204,
            "body": f"No NBA playoff stats found for {today}."
        }

    # Flatten all rows
    df = pd.json_normalize(data)

    # Send header as first record (optional; useful if S3 files are new each day)
    fh = boto3.client('firehose')
    header = ','.join(df.columns) + '\n'
    fh.put_record(
        DeliveryStreamName=FIREHOSE_NAME,
        Record={"Data": header}
    )

    # Send each stat as CSV line (no nested JSON, just flat CSV)
    sent = 0
    for _, row in df.iterrows():
        msg = ','.join([str(v) if v is not None else '' for v in row]) + '\n'
        fh.put_record(
            DeliveryStreamName=FIREHOSE_NAME,
            Record={"Data": msg}
        )
        sent += 1

    return {
        "statusCode": 200,
        "body": f"Sent {sent} records to Firehose stream {FIREHOSE_NAME} for {today}."
    }
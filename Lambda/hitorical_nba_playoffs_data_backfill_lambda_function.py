import requests
import time
import boto3
import pandas as pd
import io
from datetime import datetime

S3_BUCKET = 'nba-playoffs-historical-bucket'
OBJECT_KEY = f"raw_historical_playoffs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
API_URL = "https://api.balldontlie.io/v1/stats"

def lambda_handler(event, context):
    headers = {"Authorization": API_KEY}
    all_data = []

    # Loop through seasons 1995 to 2025
    for season in range(1995, 2026):
        print(f"Fetching playoff stats for season: {season}")
        params = {
            "seasons[]": season,
            "postseason": "true",
            "per_page": 100  # Max allowed by API
        }
        next_cursor = None

        while True:
            if next_cursor:
                params["cursor"] = next_cursor
            response = requests.get(API_URL, headers=headers, params=params, timeout=30)
            if response.status_code != 200:
                print(f"Error for season {season}: {response.status_code} {response.text}")
                break

            resp_json = response.json()
            data = resp_json.get('data', [])
            if not data:
                break

            all_data.extend(data)

            meta = resp_json.get("meta", {})
            next_cursor = meta.get("next_cursor")
            if not next_cursor:
                break
            time.sleep(0.2)  # To avoid hitting rate limits

    # Flatten JSON and convert to DataFrame
    if not all_data:
        print("No data fetched.")
        return {"statusCode": 500, "body": "No data fetched."}

    df = pd.json_normalize(all_data)

    # Save DataFrame to CSV in memory
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Save to S3 as CSV
    s3 = boto3.client('s3')
    s3.put_object(Bucket=S3_BUCKET, Key=OBJECT_KEY, Body=csv_buffer.getvalue())
    print(f"Upload complete: s3://{S3_BUCKET}/{OBJECT_KEY}")

    return {
        "statusCode": 200,
        "body": f"Fetched {len(all_data)} records and saved to s3://{S3_BUCKET}/{OBJECT_KEY}"
    }
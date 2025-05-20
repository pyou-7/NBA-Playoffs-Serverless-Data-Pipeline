# NBA Playoffs Data Pipeline (Serverless AWS)

This project implements a **serverless data engineering pipeline** on AWS, ingesting, transforming, and visualizing NBA Playoffs player, team, and game stats. It demonstrates end-to-end data automation - from real-time ingestion with Lambda and Firehose, to transformation with Glue, and analysis in Athena and Grafana.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Data Ingestion](#data-ingestion)
- [Data Transformation](#data-transformation)
- [Data Visualization](#data-visualization)
- [Event-Driven ETL Workflow Orchestration](#Event-Driven-ETL-Workflow-Orchestration)
- [Analysis & Observations](#analysis--observations)
- [Troubleshooting & Testing](#troubleshooting--testing)
- [Design Considerations](#design-considerations)
- [Future Improvements](#future-improvements)

---

## Architecture Overview

![Project Architecture Diagram](./AWS_Architecture/AWS_Architecture.png)

**Key AWS Services:**
- **API Source:** [Balldontlie NBA API](https://www.balldontlie.io/)
- **Ingestion:** AWS Lambda, Kinesis Firehose, S3
- **Orchestration:** EventBridge, Glue Workflows
- **ETL/Transformation:** AWS Glue Crawlers, Glue Jobs, Glue Data Catalog
- **Analytics:** Amazon Athena
- **Visualization:** Grafana
- **Monitoring:** CloudWatch Logs

---

## Data Ingestion

- **Historical Backfill Lambda:**  
  Extracts all NBA Playoffs player stats from 1995 up to the most current day. The data is saved as a bulk historical dataset in the S3 bucket:  
  - `nba-playoffs-historical-bucket`
- **Daily Ingestion Lambda:**  
  Runs automatically each day during the NBA Playoffs. If there are games on that day, it fetches the player stats and sends the data into Kinesis Data Firehose, which then delivers the records to the S3 bucket:  
  - `nba-playoffs-daily-stats-bucket`
- **Kinesis Data Firehose:**  
  Handles real-time streaming and delivery of daily stats from the Lambda function to S3.
- **EventBridge:**  
  Schedules and triggers the daily Lambda function to ensure data is ingested only when new games are played.
- **S3 Buckets:**  
  Act as the raw data landing zones for both historical and daily NBA Playoffs stats, partitioned and organized for downstream processing.

---

## Data Transformation

- **Glue Crawlers:** Detect and catalog new raw data files in S3, updating the Athena schema.
- **Glue Jobs:** Python ETL jobs:
  - Clean, normalize, and transform raw API JSON to flat, analytics-ready tables (Parquet format).
  - Partition by year/month for efficient querying.
  - Implement data quality checks (e.g., NULL checks, type casts).
  - Use a **staging table** pattern to only process new daily data before appending to the "prod" table.
- **Glue Workflows:** Orchestrate the ETL pipeline: Crawler → Staging → DQ → Prod Table.

---

## Data Visualization

- **Athena:** Query and analyze cleaned NBA stats (player, team, game metrics).
- **Grafana:** Visualize key metrics—e.g., team scoring trends, player performance, conference comparisons - using Athena as a data source.

---

## Event-Driven ETL Workflow Orchestration
![Workflow Architecture Diagram](./Pipeline_Architecture/Pipeline_Workflow.png)
This project utilizes an automated, event-driven ETL pipeline to process NBA Playoffs player stats as soon as new daily data lands in the `nba-playoffs-daily-stats-bucket` S3 bucket. The workflow is orchestrated using AWS Glue workflows and consists of the following sequence:

1. **Trigger:**  
   The workflow is triggered automatically whenever new files are created in the `nba-playoffs-daily-stats-bucket` (via Kinesis Firehose after Lambda ingestion).
2. **Crawl Raw Data:**  
   - **Glue Crawler** scans the bucket, cataloging new files and updating the Glue Data Catalog with any new schema changes.
3. **Delete Staging Table:**  
   - Existing staging tables and their data are dropped to ensure that only the new batch (previous 24 hours) is processed in the next steps.
4. **Create Staging Table:**  
   - New data from the daily raw bucket is loaded and transformed into a staging Parquet table, ready for validation.
5. **Data Quality Checks:**  
   - Automated scripts run data quality (DQ) checks on the new staging table, validating fields like player name, team abbreviation, game date, and points to ensure there are no missing, null, or duplicated values.
6. **Publish to Prod Table:**  
   - If all data quality checks pass, the new batch of daily data is **appended** to the production Parquet table (`prod` table).
7. **Workflow Monitoring:**  
   - Each job step is monitored via AWS CloudWatch and Glue triggers. If a step fails, subsequent steps do not run.

This event-driven ETL architecture ensures timely, reliable, and scalable processing of NBA Playoffs stats with minimal manual intervention.

---

## Analysis & Observations

- Automated end-to-end pipeline: new data flows from API to dashboard with no manual intervention.
- Incremental "staging → prod" table design ensures no data is reprocessed, supporting daily updates at scale.
- Data quality is maintained with ETL checks (NULLs, invalid types, duplicates).

---

## Troubleshooting & Testing

- **CloudWatch Logs:** Monitors Lambda & Glue job executions, error tracking.
- **Glue Job Debugging:** Includes test cases for ETL logic and schema validation.
- **SQL Testing:** Validated Athena queries against sample data before deployment.

---

## Design Considerations

- **Event-driven, serverless:** Entire pipeline scales with data volume, no servers to manage.
- **IAM Security:** Roles limited by least privilege for Lambda, Firehose, Glue, Athena.
- **Partitioning:** Year/month partitions optimize Athena cost/performance.
- **Incremental Loads:** New daily snapshots processed without re-ingesting history.

---

## Future Improvements

- Add NBA regular season data and combine with playoffs.
- Enhance data quality rules (e.g., fuzzy matching for player names).
- Build more advanced analytics (e.g., win prediction, player impact scores).
- Automate dashboard updates and add email/SNS alerts for failed pipeline steps.
- Add CI/CD for deployment (e.g., using AWS CDK or Terraform).
- Package pipeline for easy deployment (CloudFormation, SAM, etc).

---

## Getting Started

1. Clone this repo.
2. Review the Lambda, Glue job, and SQL scripts.
3. Deploy architecture in your AWS account using included IaC files (coming soon).
4. Connect Grafana to Athena, run provided queries for your dashboards.

---

## Contact

Questions? Contact [Your Name] | [Your LinkedIn] | [Your Email]

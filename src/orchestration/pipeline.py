import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dagster import job, op, ScheduleDefinition, Failure, get_dagster_logger
import subprocess
import asyncio

from src.scrape.telegram_scraper import main as scrape_main
from src.enrichment.yolo_enrich import main as yolo_main

@op
def scrape_telegram_data():
    logger = get_dagster_logger()
    try:
        logger.info("Starting Telegram scraping...")
        asyncio.run(scrape_main())
        logger.info("Scraping complete.")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise Failure(f"Scraping failed: {e}")

@op
def load_raw_to_postgres():
    logger = get_dagster_logger()
    try:
        logger.info("Data is loaded to Postgres during scraping. Skipping explicit load step.")
    except Exception as e:
        logger.error(f"Loading failed: {e}")
        raise Failure(f"Loading failed: {e}")

@op
def run_dbt_transformations():
    logger = get_dagster_logger()
    try:
        logger.info("Running dbt transformations via Docker Compose...")
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        result = subprocess.run(
            [
                'docker-compose', 'run', '--rm', 'app',
                'dbt', 'run',
                '--project-dir', '/app/src/dbt',
                '--profiles-dir', '/app/src/dbt'
            ],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        logger.info(result.stdout)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise Failure(f"dbt run failed: {result.stderr}")
        logger.info("dbt transformations complete.")
    except Exception as e:
        logger.error(f"dbt failed: {e}")
        raise Failure(f"dbt failed: {e}")

@op
def run_yolo_enrichment():
    logger = get_dagster_logger()
    try:
        logger.info("Starting YOLO enrichment...")
        yolo_main()
        logger.info("YOLO enrichment complete.")
    except Exception as e:
        logger.error(f"YOLO enrichment failed: {e}")
        raise Failure(f"YOLO enrichment failed: {e}")

@job
def medical_insights_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

medical_insights_schedule = ScheduleDefinition(
    job=medical_insights_pipeline,
    cron_schedule="0 0 * * *",
    name="daily_medical_insights_pipeline"
) 
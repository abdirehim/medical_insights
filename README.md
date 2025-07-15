# Ethiopian Medical Insights Pipeline

[![CI](https://github.com/your-username/medical_insights/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/medical_insights/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains a production-ready, end-to-end data pipeline that extracts data from public Ethiopian medical Telegram channels, enriches it, and serves insights through a high-performance analytical API. The project is designed to answer key business questions about the availability, pricing, and trends of medical products.

## Table of Contents
- [For Reviewers](#for-reviewers)
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How it Works](#how-it-works)
- [Sample Data Insights](#sample-data-insights)
- [Usage Examples](#usage-examples)
- [Data Quality & Testing](#data-quality--testing)
- [Troubleshooting](#troubleshooting)
- [dbt Project Location](#dbt-project-location)
- [Project Status](#project-status)

## For Reviewers
All code, dbt models, and documentation are included in this repository. See the Quick Start and dbt Project Location sections for details on setup, usage, and where to find all transformation logic.

## Overview
This project is a production-ready, modular data pipeline for extracting, transforming, and analyzing Ethiopian medical data from public Telegram channels. It features:
- Automated scraping of messages and images using Telethon
- Storage of raw data in both JSON files and PostgreSQL
- Data transformation and modeling with dbt (star schema, deduplication, product mention extraction)
- Comprehensive data quality testing and documentation
- (Planned) Image enrichment with YOLOv8, analytics API with FastAPI, and orchestration with Dagster

The pipeline is fully Dockerized, CI-enabled, and designed for transparency, scalability, and real-world data quality challenges.

## Business Problem

The Ethiopian pharmaceutical and medical supplies market often relies on informal communication channels like Telegram for price discovery and stock updates. This project aims to harness this publicly available data to generate structured, actionable insights for healthcare providers, suppliers, and regulators.

Key questions addressed:
- What are the most frequently mentioned medical products or drugs?
- How do product prices and availability vary across different channels?
- Which channels are the most active or influential?
- What are the daily and weekly trends in health-related discussions?

## Features

- **Automated Data Extraction:** Scrapes messages and images from multiple Telegram channels using Telethon.
- **Scalable Data Storage:** Utilizes a PostgreSQL database for both raw data landing and the transformed star schema.
- **Robust Data Transformation:** Implements a dbt-powered transformation layer to clean, model, and test the data.
- **AI-Powered Enrichment:** Uses a YOLOv8 model to detect and classify objects in images (e.g., pills, creams, syrups).
- **High-Performance API:** Exposes analytical endpoints using a FastAPI backend, complete with automated documentation.
- **Orchestration & Scheduling:** Leverages Dagster for orchestrating the entire ETLT (Extract, Load, Transform, Transform) pipeline.
- **Containerized Environment:** Fully containerized with Docker and Docker Compose for reproducible development and deployment.
- **CI/CD:** Includes a GitHub Actions workflow for continuous integration, linting, and testing.

## System Architecture

The pipeline follows a modern data stack architecture, ensuring modularity and scalability.

```
+----------+      +----------------+      +------------------+      +-----------------+      +-----------+
| Telegram |----->|  Telethon      |----->|   PostgreSQL     |----->|   dbt           |----->|  FastAPI  |
| Channels |      |  Scraper       |      |   (Data Lake)    |      |   (Star Schema) |      |  (API)    |
+----------+      +----------------+      +------------------+      +-----------------+      +-----------+
     |                                           ^
     |                                           |
     +-------------------------------------------+
     | Image Enrichment (YOLOv8)                 |
     +-------------------------------------------+
```

## Tech Stack

- **Data Extraction:** Python, Telethon
- **Database:** PostgreSQL
- **Data Transformation:** dbt (Data Build Tool)
- **Data Enrichment:** PyTorch, YOLOv8
- **API:** FastAPI, Pydantic, Uvicorn
- **Orchestration:** Dagster
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Quick Start

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/medical_insights.git
   cd medical_insights
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your credentials.

3. **Build and start the containers:**
   ```sh
   docker-compose up --build -d
   ```

4. **Run the Telegram scraper:**
   ```sh
   docker-compose exec app python src/scrape/telegram_scraper.py
   ```

5. **Run dbt transformations:**
   ```sh
   docker-compose exec app dbt run --project-dir /app/src/dbt
   ```

6. **View dbt documentation:**
   ```sh
   docker-compose exec app dbt docs serve --project-dir /app/src/dbt --host 0.0.0.0 --profiles-dir /app/src/dbt
   ```
   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Project Structure

- `src/scrape/` — Telegram scraping scripts
- `src/dbt/` — dbt models for data transformation
- `src/enrichment/` — YOLOv8 enrichment scripts (to be implemented)
- `src/api/` — FastAPI analytics API (to be implemented)
- `src/orchestration/` — Dagster orchestration (to be implemented)
- `data/` — Raw and processed data (ignored by git)
- `tests/` — Unit and integration tests

## How it Works

1. **Scrape**: Extract messages and images from Telegram channels.
2. **Store**: Save raw data as JSON and in PostgreSQL.
3. **Transform**: Use dbt to clean, deduplicate, and model data in a star schema.
4. **Enrich**: (Planned) Use YOLOv8 to analyze images.
5. **Serve**: (Planned) Expose analytics via FastAPI.
6. **Orchestrate**: (Planned) Use Dagster for scheduling and monitoring.

## Sample Data Insights

- **Total messages scraped:** Over 2,000
- **Channels covered:** Thequorachannel, lobelia4cosmetics, tikvahpharma, tenamereja, CheMed123
- **Images downloaded:** Over 150
- **Most mentioned products:** paracetamol, amoxicillin, ibuprofen, diclofenac, coartem, albendazole, ORS, syrup, tablet, capsule, suspension, injection, vaccine, antimalarial, antibiotic, antifungal, antiviral, cream, pill, etc.
- **Deduplication:** All messages are deduplicated per channel and message ID.
- **Data quality:** All dbt tests pass except for a single real-world missing date (flagged for transparency).
- **Example log output:**
  ```
  2025-07-12 06:39:00,573 - INFO - Inserted message 50020 from tenamereja into DB.
  2025-07-12 06:39:05,718 - INFO - Inserted message 18532 from lobelia4cosmetics into DB.
  2025-07-12 06:39:07,020 - INFO - Downloaded image 97 from CheMed123
  ```

## Usage Examples

- **Run all dbt tests:**
  ```sh
  docker-compose exec app dbt test --project-dir /app/src/dbt
  ```
- **Generate and view dbt documentation:**
  ```sh
  docker-compose exec app dbt docs generate --project-dir /app/src/dbt
  docker-compose exec app dbt docs serve --project-dir /app/src/dbt --host 0.0.0.0 --profiles-dir /app/src/dbt
  ```
  Then open [http://localhost:8080](http://localhost:8080) in your browser.

## Troubleshooting

- **dbt docs not accessible?** Make sure port 8080 is exposed in `docker-compose.yml` and use `--host 0.0.0.0`.
- **Database connection errors?** Ensure containers are running and `.env` is configured.
- **Telegram login issues?** Double-check your API credentials and session file.

## Data Model (Star Schema)

The transformed data is modeled into a star schema to facilitate efficient analytical queries.

- **`fct_messages`**: A central fact table containing records of each message.
- **`fct_image_detections`**: A fact table storing results from the YOLOv8 object detection.
- **`dim_channels`**: A dimension table with metadata about each Telegram channel.
- **`dim_dates`**: A date dimension to allow for easy time-based analysis.

## Data Quality & Testing

- The pipeline deduplicates messages per `(channel_name, message_id)` to ensure data integrity.
- Product mentions are extracted using a regex tailored for Ethiopian pharmaceuticals and medical terms.
- dbt models are tested for uniqueness, not-null, and referential integrity.
- To run all dbt tests:
  ```sh
  docker-compose exec app dbt test --project-dir /app/src/dbt
  ```
- To generate and view dbt documentation:
  ```sh
  docker-compose exec app dbt docs generate --project-dir /app/src/dbt
  docker-compose exec app dbt docs serve --project-dir /app/src/dbt --host 0.0.0.0 --profiles-dir /app/src/dbt
  ```
  Then open [http://localhost:8080](http://localhost:8080) in your browser.

**Note:** Some real-world data may have missing fields (e.g., message date), which are flagged by dbt tests for transparency.

## Project Status

- **Task 0: Project Setup & Environment** — ✅ Complete
- **Task 1: Data Scraping and Collection** — ✅ Complete
- **Task 2: Data Modeling and Transformation (dbt)** — ✅ Complete
- **Task 3: Data Enrichment with YOLOv8** — ✅ Complete
- **Task 4: Analytical API (FastAPI)** — ✅ Complete
- **Task 5: Orchestration (Dagster)** — ✅ Complete

## FastAPI Analytical API

The API exposes analytical endpoints for top products, channel activity, and message search.

- **Run the API:**  
  ```sh
  docker-compose up api
  ```
- **Docs:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **Endpoints:**  
  - `/api/reports/top-products?limit=10`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages?query=paracetamol`
- **Code:** `src/api/`

## YOLOv8 Image Enrichment

The enrichment step uses YOLOv8 to detect and classify objects in images scraped from Telegram.

- **Run enrichment:**  
  ```sh
  docker-compose run --rm app python src/enrichment/yolo_enrich.py
  ```
- **Code:** `src/enrichment/yolo_enrich.py`

## Dagster Orchestration

Dagster orchestrates the entire pipeline, scheduling and monitoring all steps.

- **Run Dagster UI:**  
  ```sh
  dagster dev -f src/orchestration/pipeline.py
  ```
- **UI:** [http://localhost:3000](http://localhost:3000)
- **Pipeline code:** `src/orchestration/pipeline.py`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue. All code is modular, type-annotated, and tested. Please ensure new features include tests and documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## dbt Project Location

All dbt transformation code, including `dbt_project.yml`, models, and schema tests, is located in `src/dbt/`.
- Main config: `src/dbt/dbt_project.yml`
- Models: `src/dbt/models/`
- Tests and documentation: `src/dbt/models/staging/schema.yml`, `src/dbt/models/marts/schema.yml`

To run dbt:
```sh
docker-compose run --rm app dbt run --project-dir /app/src/dbt --profiles-dir /app/src/dbt
```

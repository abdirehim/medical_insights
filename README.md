# Ethiopian Medical Insights Pipeline

[![CI](https://github.com/your-username/medical_insights/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/medical_insights/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains a production-ready, end-to-end data pipeline that extracts data from public Ethiopian medical Telegram channels, enriches it, and serves insights through a high-performance analytical API. The project is designed to answer key business questions about the availability, pricing, and trends of medical products.

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

## Project Structure

```
medical_insights/
├── .github/            # CI/CD workflows
├── data/               # Raw data (ignored by git)
├── src/
│   ├── api/            # FastAPI application
│   ├── dbt/            # dbt models and tests
│   ├── enrichment/     # YOLOv8 image enrichment scripts
│   ├── orchestration/  # Dagster pipeline definitions
│   └── scrape/         # Telegram scraper
├── tests/              # Unit and integration tests
├── .env                # Environment variables (local)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.10+ (for local development outside Docker)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/medical_insights.git
    cd medical_insights
    ```

2.  **Create the environment file:**
    Duplicate the `.env.example` to `.env` and fill in your credentials.
    ```bash
    cp .env.example .env
    ```
    You will need to provide:
    - `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`: Your Telegram API credentials.
    - `DATABASE_URL`: The connection string for the PostgreSQL database (defaults should work with Docker).

3.  **Build and run the containers:**
    ```bash
    docker-compose up --build -d
    ```
    This command will build the Docker image, start the application and database containers, and run the services in the background.

## Usage

### Running the Pipeline

The data pipeline is orchestrated by Dagster. Once the containers are running, you can access the Dagster UI to monitor and trigger pipeline runs.

- **Dagster UI:** [http://localhost:3000](http://localhost:3000)

From the UI, you can manually execute the `medical_insights_job` or wait for its scheduled runs.

### Accessing the API

The FastAPI application provides several endpoints for accessing the processed data.

- **API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

#### Example Endpoints:

- **Get Top 10 Mentioned Products:**
  ```bash
  curl http://localhost:8000/api/reports/top-products?limit=10
  ```

- **Get Channel Activity:**
  ```bash
  curl http://localhost:8000/api/channels/Chemed/activity
  ```

- **Search Messages:**
  ```bash
  curl http://localhost:8000/api/search/messages?query=paracetamol
  ```

## Running Tests

To run the entire test suite (unit and integration tests), execute the following command:

```bash
docker-compose exec app pytest
```

## Data Model (Star Schema)

The transformed data is modeled into a star schema to facilitate efficient analytical queries.

- **`fct_messages`**: A central fact table containing records of each message.
- **`fct_image_detections`**: A fact table storing results from the YOLOv8 object detection.
- **`dim_channels`**: A dimension table with metadata about each Telegram channel.
- **`dim_dates`**: A date dimension to allow for easy time-based analysis.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

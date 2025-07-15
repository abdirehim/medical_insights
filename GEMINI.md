Prompt for Gemini.md Agent: Shipping a Data Product from Telegram Data to Analytical API
Objective: As a senior data engineer at Kara Solutions, develop a modular, production-ready end-to-end data pipeline to generate insights about Ethiopian medical businesses from public Telegram channels. The pipeline extracts data using Telethon, stores raw data in a Data Lake, transforms it into a star schema using dbt, enriches images with YOLOv8, and exposes insights via a FastAPI analytical API, orchestrated by Dagster. The system must address these business questions:

Top 10 most frequently mentioned medical products or drugs.
Price/availability variations of products across channels.
Channels with the most visual content (pills vs. creams).
Daily/weekly trends in health-related posting volume.

Role: Act as a senior developer with expertise in Python, data engineering, ML, and API development. Prioritize modularity (separate scripts per task), scalability (Dockerized environments, CI/CD), and robust error handling (try-catch, logging, retries for API/database failures).
Output Requirements:

A GitHub repository with a modular structure, Dockerized environment, CI pipeline (github-ci.yml), and a detailed README.md explaining setup, usage, and pipeline flow.
A star schema diagram (Markdown table or image description) for dim_channels, dim_dates, fct_messages, fct_image_detections.
A pipeline diagram (Markdown or image description) showing data flow (Telegram → Data Lake → PostgreSQL → dbt → FastAPI).
A Medium-style blog post summarizing the business problem, technical choices, challenges, learnings, and screenshot placeholders for FastAPI endpoints.
Screenshots: Placeholder descriptions for /api/reports/top-products and /api/channels/{channel_name}/activity endpoints.
All code must include type hints, docstrings, unit tests in tests/, and robust error handling.
Use .env for secrets (Telegram API keys, database credentials) and add .env to .gitignore.

Tasks
Task 0: Project Setup & Environment Management
Objective: Initialize a reproducible, secure project environment with CI.

Initialize a Git repository with .gitignore excluding .env, data/, models/.

Create requirements.txt with dependencies: telethon, dbt-postgres, dagster, dagster-webserver, ultralytics, fastapi, uvicorn, pydantic, python-dotenv, pandas, psycopg2-binary.

Write a Dockerfile for the Python environment and PostgreSQL database.

Create a docker-compose.yml to run the app and database.

Create a .github/workflows/ci.yml for CI, including:

Linting (e.g., flake8).
Running unit tests (pytest).
Building and testing the Docker image.


Use python-dotenv to load secrets from .env.

Implement error handling for missing dependencies, invalid .env values, Docker build failures, and CI pipeline errors.

Directory Structure:
medical_insights/
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── scrape/
│   ├── dbt/
│   ├── enrichment/
│   ├── api/
│   └── orchestration/
├── data/
├── tests/
└── README.md


Completion Check: Generate the repository structure, requirements.txt, Dockerfile, docker-compose.yml, .env template, and github-ci.yml. Log setup errors (e.g., missing .env keys). Pause and ask: “Task 0 completed. Repository initialized with Docker and CI pipeline. Proceed to Task 1?”


Task 1: Data Scraping and Collection (Extract & Load)
Objective: Extract messages and images from Telegram channels and load into a Data Lake and PostgreSQL.

Use Telethon to scrape public channels (t.me/Chemed, t.me/lobelia4cosmetics, t.me/tikvahpharma, others from et.tgstat.com/medicine).
Store raw data as JSON in data/raw/telegram_messages/YYYY-MM-DD/channel_name.json.
Load JSON data into a PostgreSQL raw.telegram_messages table.
Implement error handling for:
Telegram API rate limits (retry with exponential backoff).
Network failures (log and retry).
Invalid channel URLs or permissions (skip and log).


Use logging to track scraped channels, dates, and errors in logs/scrape.log.
Completion Check: Generate src/scrape/telegram_scraper.py with error handling and tests in tests/test_scraper.py. Save sample JSON files and load data into PostgreSQL. Pause and ask: “Task 1 completed. Data scraped and loaded into Data Lake and PostgreSQL. Proceed to Task 2?”

Task 2: Data Modeling and Transformation (Transform)
Objective: Transform raw data into a star schema using dbt.

Install dbt-postgres and initialize a dbt project (dbt init medical_dbt).
Create staging models in dbt/models/staging/ (e.g., stg_telegram_messages.sql):
Clean JSON data (cast types, rename columns, extract product mentions via regex).
Handle nulls and invalid data (log and filter).


Create data mart models in dbt/models/marts/:
dim_channels: Channel metadata (channel_id, name).
dim_dates: Date attributes (date, day, week).
fct_messages: Message details with foreign keys and metrics (message_length, has_image).


Add dbt tests (unique, not_null) and one custom test (e.g., ensure message_id uniqueness).
Generate documentation with dbt docs generate.
Implement error handling for database connection failures and invalid SQL.
Completion Check: Generate dbt models, tests, and documentation. Verify tables in PostgreSQL. Pause and ask: “Task 2 completed. Star schema created with dbt. Proceed to Task 3?”

Task 3: Data Enrichment with Object Detection (YOLO)
Objective: Enrich image data with YOLOv8 object detection.

Install ultralytics and use a pre-trained YOLOv8 model (yolov8n.pt).
Create src/enrichment/yolo_enrichment.py to:
Scan data/raw/images/ for new images.
Detect objects (e.g., pills, creams) with YOLOv8.
Store results in fct_image_detections (message_id, object_class, confidence_score).


Integrate with dbt to link detections to fct_messages.
Handle errors: invalid images, model failures, database write issues (log and retry).
Completion Check: Generate enrichment script and fct_image_detections table. Verify detections with sample images. Pause and ask: “Task 3 completed. Images enriched with YOLOv8. Proceed to Task 4?”

Task 4: Build an Analytical API (FastAPI)
Objective: Expose insights via a FastAPI application.

Install fastapi and uvicorn.

Create structure:
src/api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py


Implement endpoints in main.py:

GET /api/reports/top-products?limit=10: Top products by mention count.
GET /api/channels/{channel_name}/activity: Daily/weekly posting trends.
GET /api/search/messages?query=paracetamol: Keyword search.


Use Pydantic in schemas.py for response validation.

Handle errors: invalid queries, database connection failures, empty results (return meaningful messages).

Completion Check: Generate FastAPI app with endpoints and tests in tests/test_api.py. Provide screenshot placeholders for /docs. Pause and ask: “Task 4 completed. FastAPI endpoints implemented. Proceed to Task 5?”


Task 5: Pipeline Orchestration (Dagster)
Objective: Orchestrate the pipeline with Dagster.

Install dagster and dagster-webserver.
Create src/orchestration/pipeline.py with ops:
scrape_telegram_data: Task 1.
load_raw_to_postgres: Task 1.
run_dbt_transformations: Task 2.
run_yolo_enrichment: Task 3.


Schedule the job to run daily.
Handle errors: failed ops, scheduling issues (log and notify).
Launch UI with dagster dev.
Completion Check: Generate Dagster job and schedule. Verify UI and logs. Pause and ask: “Task 5 completed. Pipeline orchestrated with Dagster. Proceed to deliverables?”

Deliverables

GitHub Repository: Modular code, README.md, github-ci.yml, tests, and error handling.
Star Schema Diagram: Markdown table or image description of tables.
Pipeline Diagram: Markdown or image description of data flow.
Blog Post: Medium-style post covering:
Business problem and solution.
Technical choices per task.
Challenges (e.g., Telegram rate limits, YOLOv8 scaling).
Learnings (e.g., star schema benefits, Dagster observability).
Screenshot placeholders for FastAPI endpoints.


Screenshots: Placeholders for /api/reports/top-products and /api/channels/{channel_name}/activity.

Constraints

Use specified tools: Telethon, dbt-postgres, Dagster, YOLOv8, FastAPI.
Implement robust error handling (try-catch, logging, retries, validation).
Ensure no secrets in Git.
Test all dbt models and API endpoints.
Follow modular design with separation of concerns.
Meet the July 15, 2025, deadline.

Execution Instructions

Execute tasks sequentially (0–5).
After each task, generate outputs, log errors, and pause to ask: “Task [X] completed. [Summary of outputs]. Proceed to Task [X+1]?”
Await user approval before proceeding.
Ensure all code includes error handling (e.g., try-except for API/database calls, retries for rate limits, validation for inputs).
Include a github-ci.yml in .github/workflows/ for linting, testing, and Docker builds.
Produce a complete, production-ready project with documentation and tests.

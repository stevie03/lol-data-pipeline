# League of Legends Automated Data Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-Data_Warehouse-4285F4?logo=google-cloud&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Data_Modeling-FF694B?logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE?logo=apache-airflow&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=github-actions&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-Visualization-4285F4?logo=looker&logoColor=white)

![Data Pipeline Architecture](assets/average_kda_chart.png)

## Project Overview
This is an end-to-end Data Engineering project designed to automatically extract, load, and transform my personal League of Legends match history into a cloud data warehouse for visualization. 

This project utilizes a **Hybrid ETL/ELT Architecture** powered by a containerized orchestration engine. Python acts as the initial ETL engine to extract, clean, and flatten raw JSON data from the Riot API. Once the structured data is safely in the data warehouse, **dbt** takes over as the ELT engine to calculate advanced business metrics and moving averages. The entire workflow is managed by **Apache Airflow** running inside **Docker**, ensuring my Looker Studio dashboard is always up-to-date with accurate, analytics-ready gaming stats.

## Architecture & Tech Stack

This pipeline implements a multi-tier data processing workflow (Silver to Gold layer):

1. **Extract, Transform & Load (Python) - *The Silver Layer*:**
   * Fetches recent match IDs and detailed game data from the **Riot Games API**.
   * Flattens complex JSON responses and applies initial business logic (e.g., determining 'Remake' vs 'Win/Loss', formatting UNIX timestamps).
   * Loads the structured data into a **Google Cloud BigQuery** `matches` table. Implements idempotent "Smart Load" logic to prevent duplicate row insertions by checking existing IDs.
2. **Advanced Analytics (dbt) - *The Gold Layer*:**
   * Utilizes **dbt (Data Build Tool)** to apply complex analytical logic directly within the data warehouse.
   * Securely handles division by zero for "perfect games" using `NULLIF` and data aggregation strategies.
   * Implements **advanced SQL Window Functions** (`OVER`, `ORDER BY UNIX_DATE`, `RANGE`) to calculate a **7-day rolling average KDA**. This approach accurately handles "sparse data" (days without recorded matches) by interpolating gaps, revealing true long-term performance trends rather than erratic daily spikes.
3. **Orchestration & Containerization (Docker + Apache Airflow):**
   * The local development environment is fully containerized using **Docker Compose**.
   * **Apache Airflow** acts as the overarching orchestrator, defining the dependency graph (DAG): ensuring the dbt transformations *only* run after the Python extraction successfully completes. Features built-in task retries for API rate-limiting handling.
4. **Visualize (Looker Studio):**
   * Connects directly to the dbt-generated models to visualize time-series performance, daily average KDAs, and overall trends.
5. **CI/CD Execution (GitHub Actions):**
   * Features an on-demand CI/CD workflow (`workflow_dispatch`). A cloud runner dynamically injects secure credentials, installs dependencies, and runs the pipeline directly from the repository, demonstrating cloud-native deployment capabilities.

## Features
* **Hybrid ETL/ELT Architecture:** Python handles the Extract and initial Transform tasks (acting as the Silver layer), while dbt takes over for the heavy analytical ELT transformations (Window Functions, rolling averages) to build the Gold reporting layer.
* **Idempotent Data Ingestion:** Safely re-runnable Python script that only inserts *new* matches.
* **Declarative Data Modeling:** SQL-based transformations built with dbt, ensuring data quality and version control for analytics.
* **Robust Orchestration:** Apache Airflow DAGs manage task dependencies and automatic retries in an isolated Linux container environment.
* **Secure Credential Management:** All API keys and Google Cloud permissions are securely managed via GitHub Secrets or `.env` files completely hidden via `.gitignore`.

## Setup & Environment Variables
If you want to replicate this project, you will need **Docker Desktop** installed, and the following secrets stored in your environment (`.env`) or GitHub Repository Secrets:

* `RIOT_API_KEY`: Your personal/development Riot Games API Key.
* `RIOT_PUUID`: The specific player's PUUID to track.
* `PLAYER_NAME`: Display name of the player.
* `GCP_PROJECT_ID`: Your Google Cloud Project ID (e.g., `lol-data-project-123`).
* `GOOGLE_APPLICATION_CREDENTIALS`: The full JSON content of your Google Cloud Service Account key.

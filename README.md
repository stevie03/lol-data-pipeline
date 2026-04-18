# League of Legends Automated Data Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-Data_Warehouse-4285F4?logo=google-cloud&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=github-actions&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-Data_Viz-F4B400?logo=looker&logoColor=white)

## Project Overview
This is an end-to-end Data Engineering project designed to automatically extract, transform, and load (ETL) my personal League of Legends match history into a cloud data warehouse for visualization. 

The pipeline runs completely hands-free on a daily schedule, ensuring that my Looker Studio dashboard is always up-to-date with my latest gaming stats without any duplicate records.

## Architecture & Tech Stack

1. **Extract:** Fetching recent match IDs and detailed game data from the **Riot Games API**.
2. **Transform:** Flattening complex JSON responses and filtering specific participant data (KDA, Champion played, Win/Loss, etc.) using **Python**.
3. **Load:** Writing the cleaned data into **Google Cloud BigQuery**. The script implements a "Smart Load" (Idempotent) logic: it checks existing `match_id`s in the warehouse to prevent duplicate row insertions.
4. **Automate:** A **GitHub Actions** CI/CD workflow runs the Python script automatically every night at 03:00 UTC.
5. **Visualize:** **Looker Studio** connects directly to the BigQuery dataset to display real-time win rates, KDA progression, and most played champions.

## Features
* **Idempotent Data Ingestion:** Safely re-runnable script that only inserts *new* matches.
* **Serverless Execution:** Powered entirely by GitHub Actions runners.
* **Cloud Data Warehousing:** Utilizes BigQuery's free tier for efficient data storage and querying.
* **Secure Credential Management:** All API keys and Google Service Account credentials are securely managed via GitHub Secrets.

## Setup & Environment Variables
If you want to replicate this project, you will need the following secrets stored in your environment (`.env`) or GitHub Repository Secrets:

* `RIOT_API_KEY`: Your personal/development Riot Games API Key.
* `RIOT_PUUID`: The specific player's PUUID to track.
* `PLAYER_NAME`: Display name of the player.
* `GOOGLE_APPLICATION_CREDENTIALS`: The full JSON content of your Google Cloud Service Account key (with BigQuery Data Editor permissions).

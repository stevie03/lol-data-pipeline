## Project Overview

I made a project to get my League of Legends match history and put it into a data warehouse so I can see my stats.

This project uses a way of doing things called a **Hybrid ETL/ELT Architecture**. It is like a team effort between Python and **dbt**. Python gets the data from the Riot API cleans it up and makes it simple. Then **dbt** takes over. Does the hard work of calculating my stats and making sure everything is correct. The whole thing is managed by **Apache Airflow** which runs inside **Docker** so my Looker Studio dashboard is always up to date with my gaming stats.

## Architecture & Tech Stack

My project has steps to get the data from the Riot API to my dashboard:

1. **Get Data. Make it Simple (Python). *The First Step*:**

* Gets my match IDs and game data from the **Riot Games API**.

* Makes the data simple and easy to understand.

* Puts the data into a **Google Cloud BigQuery** table. It checks if the data is already there so it does not add it twice.

2. **Calculate Stats (dbt). *The Second Step*:**

* Uses **dbt** to do calculations on my data.

* Handles cases where I do not have any data.

* Calculates my **7-day average KDA**. This shows me how I am doing over time not one day at a time.

3. **Manage the Workflow (Docker + Apache Airflow):**

* My project runs inside **Docker** so it is easy to manage.

* **Apache Airflow** makes sure everything happens in the order. If something goes wrong it tries again.

4. **See My Stats (Looker Studio):**

* Connects to my data and shows me my stats.

5. **Automate the Project (GitHub Actions):**

* Runs my project automatically when I want it to. It gets the code sets up the environment and runs the project.

## Features

* **Hybrid ETL/ELT Architecture:** Python gets the data. Makes it simple and then **dbt** does the complex calculations.

* **Do Not Add Data Twice:** My project checks if the data is already there so it does not add it twice.

* **Make Sure Data is Correct:** **dbt** makes sure my data is correct and up to date.

* **Manage the Workflow:** **Apache Airflow** makes sure everything happens in the order.

* **Keep Secrets Safe:** My project keeps my API keys and other secrets safe.

## Setup & Environment Variables

If you want to make a project, like mine you need to have **Docker Desktop** installed. You need to have the following secrets:

* `RIOT_API_KEY`: Your Riot Games API Key.

* `RIOT_PUUID`: The players ID that you want to track.

* `PLAYER_NAME`: The players name.

* `GCP_PROJECT_ID`: Your Google Cloud Project ID.

* `GOOGLE_APPLICATION_CREDENTIALS`: Your Google Cloud Service Account key.

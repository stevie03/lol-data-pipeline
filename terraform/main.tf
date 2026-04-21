provider "google" {
  project = "lol-data-pipeline-493614" 
  region  = "europe-west3"         
}

resource "google_bigquery_dataset" "match_history" {
  dataset_id  = "match_history" # Itt a lényeg!
  location    = "EU"
  description = "Raw data from Riot API"
}

resource "google_service_account" "airflow_runner" {
  account_id   = "airflow-runner-sa"
  display_name = "Airflow és Python Runner robot"
}

resource "google_project_iam_member" "bq_editor" {
  project = "lol-data-pipeline-493614"
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.airflow_runner.email}"
}
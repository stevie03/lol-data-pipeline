import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import bigquery


load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
PUUID = os.getenv("RIOT_PUUID")
PLAYER_NAME = os.getenv("PLAYER_NAME")



client = bigquery.Client()

dataset_id = f"{client.project}.match_history"
table_id = f"{dataset_id}.matches"

schema = [
    bigquery.SchemaField("match_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("player_name", "STRING"),
    bigquery.SchemaField("game_mode", "STRING"),
    bigquery.SchemaField("result", "STRING"),
    bigquery.SchemaField("champion_played", "STRING"),
    bigquery.SchemaField("kills", "INTEGER"),
    bigquery.SchemaField("deaths", "INTEGER"),
    bigquery.SchemaField("assists", "INTEGER"),
    bigquery.SchemaField("gold_earned", "INTEGER"),
    bigquery.SchemaField("damage_dealt", "INTEGER"),
    bigquery.SchemaField("match_duration", "INTEGER"),
    bigquery.SchemaField("match_date", "STRING"),
]

def create_structure_if_needed():
    try:
        client.get_dataset(dataset_id)
    except:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "EU"
        client.create_dataset(dataset)
        print(f"Dataset created.")

    try:
        client.get_table(table_id)
    except:
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table)
        print(f"Table created.")

create_structure_if_needed()
existing_match_ids = set()

try:
    query = f"SELECT match_id FROM `{table_id}`"
    query_job = client.query(query)
    existing_match_ids = {row.match_id for row in query_job}
    print(f"{len(existing_match_ids)} number of matches in the table.")
except Exception as e:
    print(f"⚠️ The table is empty or an error occurred. Error: {e}")
all_rows_to_insert = []
url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?start=0&count=20&api_key={API_KEY}"
match_ids = requests.get(url, headers={"X-Riot-Token": API_KEY}).json()
for match_id in match_ids:
    if match_id in existing_match_ids:
        print(f"Skipping: {match_id} (Already exists)")
        continue
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})
    match_details = response.json()

    for participant in match_details["info"]["participants"]:
        if participant["puuid"] == PUUID:
            row = {
                "match_id": match_id,
                "player_name": PLAYER_NAME,
                "game_mode": match_details["info"]["gameMode"],
                "result": 'Remake' if match_details["info"]["gameDuration"] < 300 else ('Win' if participant["win"] else 'Loss'),
                "champion_played": participant["championName"],
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "gold_earned": participant["goldEarned"],
                "damage_dealt": participant["totalDamageDealtToChampions"],
                "match_duration": match_details["info"]["gameDuration"],
                "match_date": datetime.fromtimestamp(match_details["info"]["gameStartTimestamp"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            }
            all_rows_to_insert.append(row)


if all_rows_to_insert:
    job_config = bigquery.LoadJobConfig(schema=schema)
    job = client.load_table_from_json(all_rows_to_insert, table_id, job_config=job_config)
    job.result()  
    print(f"{len(all_rows_to_insert)} rows successfully uploaded to BigQuery.")
else:
    print("No new data to upload.")

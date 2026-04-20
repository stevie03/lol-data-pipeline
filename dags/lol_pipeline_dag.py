from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'stevie03',
    'retries': 2, 
    'retry_delay': timedelta(minutes=3), 
}

with DAG(
    dag_id='lol_daily_data_pipeline',
    default_args=default_args,
    description='LoL Data Pipeline: Python (Extract/Load) -> dbt (Transform)',
    start_date=datetime(2026, 3, 1), 
    schedule_interval='0 3 * * *',
    catchup=False, 
    tags=['league_of_legends', 'production'],
) as dag:

    run_python_extraction = BashOperator(
        task_id='extract_and_load_riot_data',
        bash_command='cd /opt/airflow/dags/lol_project && python pipeline_bq.py',
    )

    run_dbt_models = BashOperator(
        task_id='run_dbt_transformations',
        bash_command='cd /opt/airflow/dags/lol_project/lol_models && dbt run --profiles-dir .', 
    )

    run_python_extraction >> run_dbt_models
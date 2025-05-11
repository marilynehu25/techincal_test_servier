from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

from main import load_data, clean_clinicals_trials, clean_pubmed, clean_drugs, get_links, build_json

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='drug_pipeline_dag',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id='load_data', python_callable=load_data)
    t2 = PythonOperator(task_id='clean_clinicals', python_callable=clean_clinicals_trials)
    t3 = PythonOperator(task_id='clean_drugs', python_callable=clean_drugs)
    t4 = PythonOperator(task_id='clean_pubmed', python_callable=clean_pubmed)
    t5 = PythonOperator(task_id='get_links', python_callable=get_links)
    t6 = PythonOperator(task_id='build_json', python_callable=build_json)

    t1 >> [t2, t3, t4] >> t5 >> t6

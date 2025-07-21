from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='catalog_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Ingest, validate, and store product catalog data',
) as dag:

    def ingest_catalog():
        path = '/opt/airflow/data/catalog_raw.json'
        df = pd.read_json(path)
        df.to_csv('/opt/airflow/data/catalog_stage.csv', index=False)
        logger.info("✅ Catalog ingested")

    def validate_catalog():
        df = pd.read_csv('/opt/airflow/data/catalog_stage.csv')
        if df.isnull().any().any():
            raise ValueError("❌ Found null values!")
        logger.info("✅ Validation passed")

    def store_catalog():
        df = pd.read_csv('/opt/airflow/data/catalog_stage.csv')
        df.to_parquet('/opt/airflow/data/catalog_final.parquet', index=False)
        logger.info("✅ Data stored")

    t1 = PythonOperator(task_id='ingest_catalog_data', python_callable=ingest_catalog)
    t2 = PythonOperator(task_id='validate_catalog_data', python_callable=validate_catalog)
    t3 = PythonOperator(task_id='store_catalog_data', python_callable=store_catalog)

    t1 >> t2 >> t3

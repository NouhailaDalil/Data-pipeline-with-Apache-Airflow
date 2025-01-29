import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime , timedelta
import requests
import pandas as pd
import pyodbc
import logging
from io import StringIO
from airflow import DAG
from airflow.operators.python import PythonOperator
from logic import raw_fetch_sales_api as rfsa
from logic import raw_store_sales_data as rssd


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                            logging.FileHandler("db_setup.log"),
                            logging.StreamHandler()])


# Set up default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'start_date': datetime(2024, 11, 1),
}

# Define the DAG
with DAG(
    'raw_api_sales_data',
    default_args=default_args,
    description='load sales data from sales API to PostgreSQL DB',
    #schedule_interval='*/10 * * * *',  
    catchup=False
) as dag:
    
    # Define PythonOperator to store sales data to Postgres DB
    fetch_api_sales_data_task = PythonOperator(
        task_id='fetch_sales_data_raw',
        python_callable=rfsa.fetch_sales_api
    )
    
    store_api_sales_data_task = PythonOperator(
        task_id='store_sales_data_raw',
        python_callable=rssd.store_api_sales_data
    )

    fetch_api_sales_data_task >> store_api_sales_data_task
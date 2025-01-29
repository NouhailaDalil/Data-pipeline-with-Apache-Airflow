import requests
import pandas as pd
import logging
from io import StringIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers.logging_helpers import setup_logging

setup_logging()

def fetch_sales_api(**kwargs):
    api_url = "https://my.api.mockaroo.com/sales"
    headers = {"X-API-Key": "cfb0eb60"}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Error fetching data, status code: {response.status_code}")
        else:  
            data = pd.read_csv(StringIO(response.text))
            data_dict = data.to_dict(orient="records")
            logging.info("Successfully fetched sales data from the API.")
             # Push data_dict to XCom
            kwargs['ti'].xcom_push(key='sales_data', value=data_dict)
            return data_dict
    except Exception as e:
        logging.error(f'Failed to fetch data from API : {e}') 
        raise
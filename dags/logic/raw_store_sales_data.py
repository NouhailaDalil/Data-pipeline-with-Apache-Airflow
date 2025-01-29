from io import StringIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
import logging
import pandas as pd
from logic import raw_fetch_sales_api
from helpers import logging_helpers
from helpers.database_helpers import connect_db, close_db, insert_data, add_schema, create_table, add_column_if_not_exists


def store_api_sales_data(**kwargs):
    data_dict = kwargs['ti'].xcom_pull(key='sales_data', task_ids='fetch_sales_data_raw')
    data = pd.DataFrame(data_dict)
    db_path = 'jdbc:postgresql://localhost:5432/postgres'
    conn = connect_db(db_path)
    try:
        ingestion_time = datetime.now()
        data["ingestion_time"] = ingestion_time
        columns = [
            "order_id","order_date","quantity","payment_method","order_status","customer_id","customer_name"
            ,"email","gender","country_code","product_id","product_name","unit_price","ingestion_time"]
        records = [(
                record["order_id"], record["order_date"], record["quantity"], record["payment_method"],
                record["order_status"], record["customer_id"], record["customer_name"],
                record["email"], record["gender"], record["country_code"], record["product_id"],
                record["product_name"], record["unit_price"], record["ingestion_time"]
            ) for _, record in data.iterrows()
        ] 
        insert_data(conn, "raw_layer.sales", columns, records)
        conn.commit()
        logging.info(f'Successfuly inserted data into raw_layer.sales table') 
    except Exception as e:
        logging.error(f'Failed to insert data to a table : {e}')
        raise
    finally:
        close_db(conn)
        logging.info('Database Closed')
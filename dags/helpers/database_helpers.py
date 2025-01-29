import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2 
from typing import List, Dict
import logging
from helpers.logging_helpers import setup_logging

# Set up logging 
#setup_logging()

def connect_db(db_path: str):
    try:
        conn = psycopg2.connect(
        host="host.docker.internal",       # ou le nom de votre conteneur Docker (ex : "postgres")
        database="postgres",  # Nom de votre base de données
        user="postgres",    # Nom d'utilisateur
        password="test123",
        port = "5432"
        )   
        logging.info("Connected to PostgreSQL database.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def close_db(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        logging.info("Closed the database connection.")

def add_schema(conn, schemas: List[str]):
    """Create schemas if they do not already exist."""
    conn = connect_db('jdbc:postgresql://localhost:5432/postgres')
    for schema in schemas:
        try:
            cur = conn.cursor()
            cur.execute(f"CREATE SCHEMA {schema};")
            conn.commit()
            cur.close()
            logging.info(f"Created schema '{schema}' if it did not exist.")
        except Exception as e:
            logging.error(f"Failed to create schema '{schema}': {e}")
            raise

def create_table(conn, schema: str, table: str, columns: Dict[str, str]):
    """Create a table with specified columns if it does not exist."""
    columns_def = ", ".join([f"{name} {type}" for name, type in columns.items()])
    create_table_sql = f"CREATE TABLE {schema}.{table} ({columns_def});"
    conn = connect_db('jdbc:postgresql://localhost:5432/postgres')
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        conn.close()
        logging.info(f"Created table '{schema}.{table}' with columns: {columns}.")
    except Exception as e:
        logging.error(f"Failed to create table '{schema}.{table}': {e}")
        raise

def add_column_if_not_exists(conn, schema: str, table: str, column: str, col_type: str):
    try:
        with conn.cursor() as cursor:
            # Vérifier si la colonne existe déjà
            col_exists_query = """
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s AND column_name = %s;
            """
            cursor.execute(col_exists_query, (schema, table, column))
            col_exists = cursor.fetchone()[0] > 0

            if not col_exists:
                # Ajouter la colonne si elle n'existe pas
                alter_table_query = f"ALTER TABLE {schema}.{table} ADD {column} {col_type};"
                cursor.execute(alter_table_query)
                conn.commit()
                logging.info(f"Added column '{column}' to table '{schema}.{table}'.")
            else:
                logging.info(f"Column '{column}' already exists in table '{schema}.{table}'.")
    except Exception as e:
        logging.error(f"Failed to add column '{column}' to table '{schema}.{table}': {e}")
        raise


def insert_data(conn, table_name: str, columns, registry):
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s' for _ in columns])

    # SQL query to insert data
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    conn = connect_db('jdbc:postgresql://localhost:5432/postgres')
    try:
        # Execute the query for each record
        cur = conn.cursor()
        cur.executemany(query, registry)
        conn.commit()
        cur.close()
        logging.info(f"Data successfully inserted into {table_name}.")
    except Exception as e:
        logging.error(f"Failed to insert data into {table_name}: {e}")
        raise
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.database_helpers import connect_db, close_db, add_schema, create_table, add_column_if_not_exists

class DatabaseManager:
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def setup_database(self):
        """Set up schemas, tables, and required columns."""
        # Connect to the database
        self.conn = connect_db(self.db_path)

        # Define schemas and tables with columns
        schemas = ['raw_layer', 'refined_layer', 'report_layer']
        raw_sales_columns = {
            "order_id": "INTEGER",
            "order_date": "DATE",
            "customer_id": "INTEGER",
            "customer_name": "VARCHAR",
            "product_id": "INTEGER",
            "product_name": "VARCHAR",
            "quantity": "INTEGER",
            "unit_price": "DECIMAL(10, 2)",
            "payment_method": "VARCHAR",
            "order_status": "VARCHAR",
            "email": "VARCHAR",
            "gender": "VARCHAR",
            "country_code": "VARCHAR"
        }

        refined_customers_columns = {
            "customer_id": "INTEGER",
            "customer_name": "VARCHAR",
            "email": "VARCHAR",
            "gender": "VARCHAR",
            "country_code": "VARCHAR"
        }

        # Add schemas
        add_schema(self.conn, schemas)

        # Create tables
        create_table(self.conn, "raw_layer", "sales", raw_sales_columns)
        create_table(self.conn, "refined_layer", "customers", refined_customers_columns)

        # Add 'ingestion_time' column if it doesn't exist
        add_column_if_not_exists(self.conn, "raw_layer", "sales", "ingestion_time", "TIMESTAMP")
        add_column_if_not_exists(self.conn, "refined_layer", "customers", "ingestion_time", "TIMESTAMP")

        # Close the connection
        close_db(self.conn)

if __name__ == "__main__":
    db_manager = DatabaseManager('jdbc:postgresql://localhost:5432/postgres')
    db_manager.setup_database()
    
import os
import random
import logging
from datetime import datetime
import uuid

import pandas as pd
import psycopg2
from psycopg2 import pool
from faker import Faker

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class BankingDataGenerator:
    def __init__(self, 
                host=None, 
                port=5432, 
                dbname=None, 
                user=None, 
                password=None,
                max_connections=10):
        """
        Initialize the Banking Data Generator
        
        Args:
            host (str): Database host
            port (int): Database port
            dbname (str): Database name
            user (str): Database username
            password (str): Database password
            max_connections (int): Maximum connection pool size
        """
        
        # Use os.getenv with fallback
        self.host = host or os.getenv('DB_HOST', 'database-2.crkkagcyym3o.us-east-1.rds.amazonaws.com')
        self.port = port or int(os.getenv('DB_PORT', 5432))
        self.dbname = dbname or os.getenv('DB_NAME', 'postgres')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', 'postgres')
        
        # Validate connection parameters
        self._validate_connection_params()
        
        # Create connection pool
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, max_connections,
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            logger.info("Connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
        
        # Initialize Faker for data generation
        self.fake = Faker()
        
        # Configuration for data generation
        self.merchant_categories = [
            "Retail", "Electronics", "Clothing", "Groceries", "Pharmacy", 
            "Entertainment", "Dining", "Travel", "Utilities", "Healthcare"
        ]
        
        self.card_types = {
            "visa": "visa",
            "mastercard": "mastercard"
        }

    def _validate_connection_params(self):
        """Validate database connection parameters"""
        missing_params = [
            param for param, value in {
                'host': self.host,
                'user': self.user,
                'password': self.password
            }.items() if not value
        ]
        
        if missing_params:
            error_msg = f"Missing required connection parameters: {', '.join(missing_params)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def create_table(self):
        """Create banking_data table if not exists"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS banking_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            uniq_id UUID NOT NULL,
            trans_type VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            amount_crr DECIMAL(10, 2) NOT NULL,
            account_holder_name VARCHAR(100) NOT NULL,
            card_presense VARCHAR(50) NOT NULL,
            merchant_category VARCHAR(50) NOT NULL,
            card_type VARCHAR(50) NOT NULL,
            card_id VARCHAR(20) NOT NULL,
            account_id UUID NOT NULL,
            account_blacklisted BOOLEAN NOT NULL,
            rules_triggered VARCHAR(100),
            rules_explanation VARCHAR(100),
            decision VARCHAR(100)
        );
        """
        connection = None
        try:
            connection = self.connection_pool.getconn()
            with connection.cursor() as cursor:
                cursor.execute(create_table_query)
                connection.commit()
                logger.info("Table 'banking_data' created or already exists")
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)

    def generate_record(self):
        """Generate a single random banking record"""
        card_type = random.choice(list(self.card_types.keys()))
        return {
            "uniq_id": self.fake.uuid4(),
            "trans_type": random.choice(["Real_time_transaction", "settlements", "dispute"]),
            "amount": round(random.uniform(10.0, 1000.0), 2),
            "amount_crr": round(random.uniform(10.0, 1000.0), 2),
            "account_holder_name": self.fake.name(),
            "card_presense": random.choice(["Present", "Not Present"]),
            "merchant_category": random.choice(self.merchant_categories),
            "card_type": card_type,
            "card_id": self.fake.credit_card_number(card_type=self.card_types[card_type]),
            "account_id": self.fake.uuid4(),
            "account_blacklisted": random.choice([True, False])
        }

    def run_rules(self, record):
        """Apply transaction rules to the record"""
        rules_result = {
            "rules_triggered": "No Rules Triggered",
            "rules_explanation": None,
            "decision": "Approved"
        }

        if (record["amount"] >= 100 and 
            not record["account_blacklisted"] and 
            record["trans_type"] == "Real_time_transaction"):
            rules_result.update({
                "rules_triggered": "Rule1",
                "rules_explanation": "User is trying to make a transaction of more than 100$",
                "decision": "Rejected"
            })
        
        elif (record["account_blacklisted"] and 
              record["trans_type"] == "Real_time_transaction"):
            rules_result.update({
                "rules_triggered": "Rule2",
                "rules_explanation": "It is a blacklisted Card",
                "decision": "Rejected"
            })
        
        return {**record, **rules_result}

    def insert_records(self, num_records=10):
        """Insert multiple records into the database"""
        connection = None
        try:
            connection = self.connection_pool.getconn()
            with connection.cursor() as cursor:
                timestamp = datetime.utcnow()
                
                for _ in range(num_records):
                    record = self.generate_record()
                    processed_record = self.run_rules(record)
                    
                    cursor.execute("""
                    INSERT INTO banking_data (
                        timestamp, uniq_id, trans_type, amount, amount_crr, 
                        account_holder_name, card_presense, merchant_category, 
                        card_type, card_id, account_id, account_blacklisted,
                        rules_triggered, rules_explanation, decision
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        timestamp, processed_record['uniq_id'], 
                        processed_record['trans_type'], processed_record['amount'], 
                        processed_record['amount_crr'], processed_record['account_holder_name'], 
                        processed_record['card_presense'], processed_record['merchant_category'],
                        processed_record['card_type'], processed_record['card_id'], 
                        processed_record['account_id'], processed_record['account_blacklisted'],
                        processed_record['rules_triggered'], 
                        processed_record['rules_explanation'], 
                        processed_record['decision']
                    ))
                
                connection.commit()
                logger.info(f"Inserted {num_records} records successfully")
        
        except Exception as e:
            logger.error(f"Error inserting records: {e}")
            if connection:
                connection.rollback()
        
        finally:
            if connection:
                self.connection_pool.putconn(connection)

    def run(self, num_iterations=10, records_per_iteration=10):
        """
        Main method to run the data generation process
        
        Args:
            num_iterations (int): Number of times to generate and insert records
            records_per_iteration (int): Number of records to generate per iteration
        """
        try:
            # Create table if not exists
            self.create_table()
            
            # Generate and insert records
            for i in range(num_iterations):
                logger.info(f"Iteration {i+1}/{num_iterations}")
                self.insert_records(records_per_iteration)
        
        except Exception as e:
            logger.error(f"Error in data generation process: {e}")
        
        finally:
            # Close connection pool
            if hasattr(self, 'connection_pool'):
                self.connection_pool.closeall()
                logger.info("Connection pool closed")

def main():
    # Example usage with default or environment variables
    generator = BankingDataGenerator()
    generator.run(num_iterations=5, records_per_iteration=20)

if __name__ == "__main__":
    main()
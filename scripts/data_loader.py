import os
import sys
from pyspark.sql import SparkSession
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_tables():
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    try:
        with engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS cities (
                    city_id INT PRIMARY KEY,
                    city_name VARCHAR(255),
                    country VARCHAR(2),
                    latitude FLOAT,
                    longitude FLOAT
                )
            """))
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS weather_measurements (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    time TIME,
                    city_id INT,
                    temperature FLOAT,
                    humidity INT,
                    pressure INT,
                    wind_speed FLOAT
                )
            """))
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

def load_data(fact_df, dim_df):
    logger.info("Starting data load process")
    try:
        dim_df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", "cities") \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .mode("overwrite") \
            .save()
        logger.info("Cities data loaded successfully")

        fact_df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", "weather_measurements") \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .mode("append") \
            .save()
        logger.info("Weather measurements data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

    logger.info("Data loading process completed")

if __name__ == "__main__":
    create_tables()

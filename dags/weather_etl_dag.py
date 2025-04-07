import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from dotenv import load_dotenv

dag_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(dag_folder, '..'))
sys.path.insert(0, project_root)

load_dotenv(os.path.join(project_root, '.env'))

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

from scripts.api_client import fetch_weather_data
from scripts.data_transformer import transform_weather_data
from scripts.data_loader import load_data, create_tables

def create_spark_session():
    return SparkSession.builder \
        .appName("WeatherETL") \
        .config("spark.jars", "/Users/stuartmills/Documents/weather-data-integration/postgresql-42.7.4.jar") \
        .config("spark.driver.extraClassPath", "/Users/stuartmills/Documents/weather-data-integration/postgresql-42.7.4.jar") \
        .config("spark.executor.extraClassPath", "/Users/stuartmills/Documents/weather-data-integration/postgresql-42.7.4.jar") \
        .config("spark.hadoop.javax.jdo.option.ConnectionDriverName", "org.postgresql.Driver") \
        .config("spark.hadoop.javax.jdo.option.ConnectionURL", f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}") \
        .config("spark.hadoop.javax.jdo.option.ConnectionUserName", DB_USER) \
        .config("spark.hadoop.javax.jdo.option.ConnectionPassword", DB_PASSWORD) \
        .master("local[*]") \
        .getOrCreate()

def etl_process():
    spark = None
    try:
        spark = create_spark_session()
        raw_data = fetch_weather_data()
        if not raw_data:
            raise ValueError("No data fetched from the API")
        fact_df, dim_df = transform_weather_data(spark, raw_data)
        load_data(fact_df, dim_df)
    except Exception as e:
        print(f"Error in ETL process: {str(e)}")
        raise
    finally:
        if spark:
            spark.stop()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    description='A DAG for weather data ETL process using Spark',
    schedule_interval=timedelta(days=1),
)

with dag:
    create_tables_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables,
    )
    
    etl_task = PythonOperator(
        task_id='weather_etl_process',
        python_callable=etl_process,
    )
    
    create_tables_task >> etl_task

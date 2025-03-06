from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlalchemy
import os

def get_ticker_quotes(ticker, interval):
    try:
        crypto = ticker
        url = f"https://api.binance.com/api/v3/klines?symbol={crypto}&interval={interval}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data, columns=[
            'Open time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume', 'ignore'])
        float_columns = ['open', 'high', 'low', 'close', 'volume',
                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                         'taker_buy_quote_asset_volume']

        df[float_columns] = df[float_columns].astype(float)
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_and_store_ticker_quotes():
    ticker = 'BNBUSDT'
    interval = '1d'
    df = get_ticker_quotes(ticker, interval=interval)
    if df is not None:
        try:
            db_url = os.getenv('DATABASE_URL')
            engine = sqlalchemy.create_engine(db_url)
            df.to_sql('ticker_quotes', engine, if_exists='append', index=False)
            print("Data stored successfully")
        except Exception as e:
            print(f"Error storing data: {e}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'get_ticker_quotes_dag',
    default_args=default_args,
    description='A simple DAG to fetch ticker quotes from Binance',
    schedule_interval=timedelta(days=1),
)

fetch_ticker_quotes_task = PythonOperator(
    task_id='fetch_ticker_quotes',
    python_callable=fetch_and_store_ticker_quotes,
    dag=dag,
)

fetch_ticker_quotes_task
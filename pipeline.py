import requests
import pandas as pd
from datetime import datetime
import os
import sqlalchemy as db

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_raw_data(self, symbol):
        full_url = f"{self.base_url}/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(full_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
        
class DataTransformer:
    def transform_raw_payload(self, raw_data):
        
        result = raw_data["chart"]["result"][0]
        
        ticker = result["meta"]["symbol"]
        timestamps = result["timestamp"]
        quote = result["indicators"]["quote"][0]
        
        extracted_data = {
            "Ticker": ticker,
            "ObservationDate" : timestamps,
            "OpenPrice" : quote["open"],
            "HighPrice" : quote["high"],
            "LowPrice" : quote["low"],
            "ClosePrice" : quote["close"],
            "Volume" : quote["volume"],
        }
        
        df = pd.DataFrame(extracted_data)
        
        df["ObservationDate"] = pd.to_datetime(df["ObservationDate"], unit="s").dt.date
        df["IngestedAt"] = datetime.now()
        return df
    

class DatabaseManager():
    def __init__(self):
        self.user = 'sa'
        self.password = os.getenv("MY_DB_PASSWORD")
        self.host = "localhost"
        self.port = '1433'
        self.db_name = 'master'
        
        connection_url = f"mssql+pyodbc://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no&TrustServerCertificate=yes"
        self.engine = db.create_engine(connection_url)
        
    def write_log(self, start_time, end_time, rows, status, error_msg=None):
        log_query = """
        INSERT INTO PipelineLog (ExecutionStart, ExecutionEnd, RowsInserted, PipelineStatus)
        VALUES (:start, :end, :rows, :status);
        """
        with self.engine.connect() as connection:
            connection.execute(
                db.text(log_query),
                {
                    "start": start_time,
                    "end": end_time,
                    "rows": rows,
                    "status": status,
                    "error": error_msg
                }
            )
            connection.commit()
            
    def insert_data(self, df):
        df.to_sql(
            name="TheCoreMarketDataTable",
            con=self.engine,
            if_exists="append",
            index=False       
        )
        
if __name__ == "__main__":
    API_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
    client = APIClient (base_url=API_BASE)
    transformer = DataTransformer()

    print("Fetching data ... ")
    raw_payload = client.fetch_raw_data('AAPL')
    
    if raw_payload:
        print("Transforming data ...")
        cleaned_df = transformer.transform_raw_payload(raw_payload)
        print("\nCleaned Data Warehouse Matrix:")
        print(cleaned_df.head())
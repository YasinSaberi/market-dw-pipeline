import requests
import pandas as pd
from datetime import datetime
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
        
if __name__ == "__main__":
    API_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
    client = APIClient (base_url=API_BASE)
    print("Fetching data ... ")
    raw_payload = client.fetch_raw_data('AAPL')
    print("Success! Raw payload type:", type(raw_payload))
    print("Keys found in the response:", raw_payload.keys())
    
    
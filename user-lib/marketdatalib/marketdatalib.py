import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import yfinance as yf


_nifty_history_url = 'https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString'

class CInfo:
    def __init__(self, name, start_date, end_date, index_name):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.index_name = index_name

    def to_dict(self):
        return {
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'index_name': self.index_name
        }

    def __repr__(self):
        return (f"{{'name':'{self.name}', 'startDate':'{self.start_date}', "
                f"'endDate':'{self.end_date}', 'indexName':'{self.index_name}'}}")
    
    def __str__(self):
        return (f"{{'name':'{self.name}', 'startDate':'{self.start_date}', "
                f"'endDate':'{self.end_date}', 'indexName':'{self.index_name}'}}")


def get_nifty_index_data(index_name: str, number_of_years: int = 5) -> pd.DataFrame:
    today = datetime.today()
    enddate = startdate = today - relativedelta(years=number_of_years)
    # enddate = min(startdate + relativedelta(years=1), today)

    base_url = f'https://www.nseindia.com/api/historical/indicesHistory?indexType={index_name}&from={{}}&to={{}}'
    nifty_data = pd.DataFrame()

    with requests.sessions.Session() as session:
        session.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"})
        
        # Get cookies in the session. The cokies will be sent in subsequent requests.
        session.get("https://www.nseindia.com/")

        while enddate < today:
            enddate = min(startdate + relativedelta(years=1), today)
            request_url = base_url.format(startdate.strftime("%d-%m-%Y"), enddate.strftime("%d-%m-%Y"))
            
            pricing_data_json = session.get(request_url).json()['data']['indexCloseOnlineRecords']
            pricing_data = pd.DataFrame.from_dict(pricing_data_json)
            nifty_data = pd.concat([nifty_data, pricing_data], ignore_index=False, axis=0)

            startdate = enddate + relativedelta(days=1)

    # Now that we have a raw dataframe, the next step is to clean it up and convert it into a format that we can use.
    # Drop unnecessary columns
    nifty_data.drop(columns=['_id', 'EOD_INDEX_NAME', 'TIMESTAMP'], inplace=True)
    # Map column names to new values

    nifty_data.rename(columns= {'EOD_TIMESTAMP': 'Date', 'EOD_OPEN_INDEX_VAL': 'Open', 'EOD_HIGH_INDEX_VAL': 'High', 'EOD_LOW_INDEX_VAL': 'Low', 'EOD_CLOSE_INDEX_VAL': 'Close'}, inplace=True)
    nifty_data.set_index('Date', inplace=True)
    # Convert the date column to datetime. The date is in the format 'dd-mmm-YYYY'
    nifty_data.index = pd.to_datetime(nifty_data.index, format='%d-%b-%Y')
    nifty_data.sort_index(inplace=True)

    return pd.DataFrame(nifty_data)

def map_scrip_to_yfin_ticker(scrip: str, exchange: str = 'NSE') -> tuple[str, yf.Ticker]:
    """
    Map scrip to yfinance ticker.
    """
    extension = '.NS'
    if exchange == 'BSE': extension = '.BO'

    return (scrip, yf.Ticker(scrip + extension))

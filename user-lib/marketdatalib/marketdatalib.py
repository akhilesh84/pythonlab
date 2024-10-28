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


def _get_cookie():
    """
    Get cookie from the website.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*'
    }

    try:
        response = requests.get('https://www.niftyindices.com/Backpage.aspx', headers=headers)  # Timeout in seconds
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return response.cookies

def get_nifty_index_data(start_date, end_date, index_name):
    """
    Get Nifty index data for the given date range and index name.
    """
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    cinfo = CInfo(index_name, start_date, end_date, index_name)

    cookies = _get_cookie()
    
    payload = '{{"cinfo":"{{\'name\':\'{name}\',\'startDate\':\'{start_date}\',\'endDate\':\'{end_date}\',\'indexName\':\'{index_name}\'}}"}}'.format(
    name=cinfo.index_name, start_date=cinfo.start_date, end_date=cinfo.end_date, index_name=cinfo.index_name)

    print("Payload: ", payload)

    print("Cookies: ", cookies)

    response = requests.post(_nifty_history_url, headers=headers, data=payload, cookies=cookies)
    return response.json()

def map_scrip_to_yfin_ticker(scrip: str, exchange: str = 'NSE') -> tuple[str, yf.Ticker]:
    """
    Map scrip to yfinance ticker.
    """
    extension = '.NS'
    if exchange == 'BSE': extension = '.BO'

    return (scrip, yf.Ticker(scrip + extension))

import requests
import json

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
        response = requests.get('https://www.niftyindices.com/Backpage.aspx', headers=headers, timeout=10)  # Timeout in seconds
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
        'Accept': '*/*'
    }

    cinfo = CInfo(index_name, start_date, end_date, index_name)

    # Convert the object to a dictionary
    cinfo_dict = cinfo.to_dict()

    # Convert the dictionary to a JSON string
    cinfo_json = json.dumps(cinfo_dict)
    # cinfo_json = json.dumps(cinfo_json)

    # Replace double quotes with single quotes
    escaped_json_string = cinfo_json.replace('"', "'")

    print(escaped_json_string)

    print({'cinfo': escaped_json_string})

    response = requests.post(_nifty_history_url, headers=headers, cookies=_get_cookie(), data={'cinfo': escaped_json_string})
    return response.json()
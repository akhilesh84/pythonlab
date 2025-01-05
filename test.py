from marketdatalib import get_nifty_index_data

import requests
session = requests.Session()
print("Session proxies:", session.proxies)

respnse = get_nifty_index_data('NIFTYBEES.NS', 5)
print(respnse)

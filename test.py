from marketdatalib import get_nifty_index_data

import requests
session = requests.Session()
print("Session proxies:", session.proxies)

respnse = get_nifty_index_data('01-Jan-2013', '01-Jan-2024', 'NIFTY 500')
print(respnse)

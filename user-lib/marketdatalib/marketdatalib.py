_nifty_history_url = 'https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString'

class CInfo:
    def __init__(self, name, start_date, end_date, index_name):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.index_name = index_name

    def __repr__(self):
        return (f"{{'name':'{self.name}', 'startDate':'{self.start_date}', "
                f"'endDate':'{self.end_date}', 'indexName':'{self.index_name}'}}")
    
    def __str__(self):
        return (f"{{'name':'{self.name}', 'startDate':'{self.start_date}', "
                f"'endDate':'{self.end_date}', 'indexName':'{self.index_name}'}}")


def __init__():
    print('This is a library file and should not be executed directly')
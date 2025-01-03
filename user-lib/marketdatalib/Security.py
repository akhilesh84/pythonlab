from enum import Enum

class SecurityType(Enum):
    MutualFund = 1,
    ETF = 2,
    Stock = 3,
    Index = 4

class Security:
    def __init__(self, name: str, code: str, security_type: SecurityType, exchange: str = 'NSE'):
        self.name = name
        self.code = code
        self.exchange = exchange

    def __repr__(self):
        return (f"{{'name':'{self.name}', 'code':'{self.code}', 'exchange':'{self.exchange}'}}")
    
    def __str__(self):
        return (f"{{'name':'{self.name}', 'code':'{self.code}', 'exchange':'{self.exchange}'}}")

    def get_historical_data(self, start_date: str, end_date: str):
        pass
    
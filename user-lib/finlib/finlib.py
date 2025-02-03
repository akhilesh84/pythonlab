import numpy as np
import numpy_financial as npf
from datetime import datetime
from babel.numbers import format_currency
from matplotlib import pyplot as plt

def format_inr(amount):
    return format_currency(amount, 'INR', locale='en_IN')

# # Function to get market capitalization of a stock
# def get_market_cap(stock_code):
#     stock_info = yf.Ticker(stock_code).info
#     return stock_info.get('marketCap', 0)

def FV(pv, r, n, t):
    """
    Calculate the future value of an investment.

    Parameters:
    pv: float - The present value of the investment
    r: float - The annual interest rate (in decimal form)
    n: int - The number of times that interest is compounded per year
    t: int - The number of years the money is invested for

    Returns:
    float - The future value of the investment
    """
    fv = pv * (1 + r/n)**(n*t)
    return fv

def calculate_terminal_value(final_cash_flow, long_term_growth_rate, discount_rate):
    terminal_value = final_cash_flow * (1 + long_term_growth_rate) / (discount_rate - long_term_growth_rate)
    return terminal_value

def calculate_intrinsic_value(future_cash_flows, discount_rate, terminal_value):
    intrinsic_value = 0
    for year, cash_flow in enumerate(future_cash_flows, start=1):
        discounted_cash_flow = cash_flow / (1 + discount_rate) ** year
        intrinsic_value += discounted_cash_flow
    intrinsic_value += terminal_value / (1 + discount_rate) ** len(future_cash_flows)
    return intrinsic_value

def calculate_real_interest_rate(nominal_interest_rate, inflation_rate):
    """
    This function calculates the real interest rate given the nominal interest rate and the inflation rate.
    This can basically be used to estimate the inflation adjusted value of an investment for which there is a fixed nominal interest rate.

    Parameters:
    nominal_interest_rate: float - The nominal interest rate (in decimal form)
    inflation_rate: float - The inflation rate (in decimal form)

    Returns:
    float - The real interest rate (in decimal form). Multiply this value by 100 to get the real interest rate as a percentage.
    """
    real_interest_rate = (nominal_interest_rate - inflation_rate) / (1 + inflation_rate)
    return real_interest_rate

def calculate_cagr(cash_flows, dates, end_value):
    # Calculate the total invested amount
    total_invested = sum(cash_flows)
    
    # Calculate the number of years for each cash flow
    years = [(dates[-1] - date).days / 365.0 for date in dates]
    
    # Calculate the weighted average of the invested amounts over time
    weighted_invested = sum(cf * year for cf, year in zip(cash_flows, years)) / total_invested
    
    # Calculate the CAGR
    cagr = (end_value / total_invested) ** (1 / weighted_invested) - 1
    return cagr

def calculate_xirr(cash_flows, dates):
    """
    Calculate the internal rate of return (IRR) for a series of cash flows that might not be periodic.

    Parameters:
    cash_flows: list - A list of cash flows for the investment
    dates: list - A list of dates for the cash flows

    Returns:
    float - The extended internal rate of return (IRR) for the investment

    Usage:
    cash_flows = [-100, 20, 30, 40, 50, 60]
    dates = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05', '2018-01-06']
    xirr = calculate_xirr(cash_flows, dates)
    """
    return npf.xirr(cash_flows, dates)

def calculate_sharpe_ratio(prices, risk_free_rate):
    # Calculate daily returns
    daily_returns = prices[1:] / prices[:-1] - 1
    
    # Calculate average daily return
    avg_daily_return = np.mean(daily_returns)
    
    # Calculate standard deviation of daily returns
    std_daily_return = np.std(daily_returns)
    
    # Annualize the average daily return and standard deviation
    annualized_return = (1 + avg_daily_return) ** 252 - 1
    annualized_std = std_daily_return * np.sqrt(252)
    
    # Calculate Sharpe Ratio
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std
    
    return sharpe_ratio

def calculate_annualized_return(prices):
    # Calculate daily returns
    daily_returns = prices[1:] / prices[:-1] - 1
    
    # Calculate average daily return
    avg_daily_return = np.mean(daily_returns)
    
    # Annualize the average daily return
    annualized_return = (1 + avg_daily_return) ** 252 - 1
    
    return annualized_return

def calculate_beta(stock_returns, benchmark_returns):
    # Calculate covariance matrix between stock returns and benchmark returns
    covariance_matrix = np.cov(stock_returns, benchmark_returns)
    
    # Extract the covariance between stock returns and benchmark returns
    covariance = covariance_matrix[0, 1]
    
    # Calculate variance of benchmark returns
    variance = np.var(benchmark_returns)
    
    # Calculate Beta
    beta = covariance / variance
    
    return beta

class FundMeta:
    moniker = None
    fund_name = None
    url = None
    
    def __init__(self, moniker, fund_name, url):
        self.moniker = moniker
        self.fund_name = fund_name
        self.url = url

def expected_portfolio_return(weights, returns):
    """
    Calculate the expected return of a portfolio.

    :param weights: List of weights of the assets in the portfolio. 
                    The weights should sum to 1.
    :param returns: List of expected returns of the assets in the portfolio.
    :return: Expected return of the portfolio.
    """
    if len(weights) != len(returns):
        raise ValueError("The number of weights must match the number of returns")
    
    if not (0.999 <= sum(weights) <= 1.001):
        raise ValueError("The sum of the weights must be 1")
    
    portfolio_return = sum(w * r for w, r in zip(weights, returns))
    return portfolio_return

def efficient_frontier(risk_free_rate, market_returns):
    """
    Plot the efficient frontier given a risk-free rate and market returns.
    
    :param risk_free_rate: The risk-free rate of return.
    :param market_returns: Array of historical returns of the market-linked security.
    """

    def calculate_statistics(returns):
        """
        Calculate the expected return and standard deviation of returns.
        
        :param returns: Array of historical returns.
        :return: Tuple of expected return and standard deviation.
        """
        expected_return = np.mean(returns)
        std_dev = np.std(returns)
        return expected_return, std_dev

    market_expected_return, market_std_dev = calculate_statistics(market_returns)
    
    weights = np.linspace(0, 1, 100)
    portfolio_returns = []
    portfolio_risks = []
    
    for w in weights:
        portfolio_return = risk_free_rate + w * ( market_expected_return -  risk_free_rate)
        portfolio_risk = w * market_std_dev
        portfolio_returns.append(portfolio_return)
        portfolio_risks.append(portfolio_risk)
    
    plt.figure(figsize=(12, 10))
    plt.scatter(portfolio_risks, portfolio_returns, c='blue', marker='o', label='Efficient Frontier')
    plt.plot(portfolio_risks, portfolio_returns, c='blue')
    plt.xlabel('Risk (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.title('Efficient Frontier with Risk-Free Asset')
    plt.legend()
    plt.grid(True)
    plt.show()

    return zip(weights, portfolio_returns, portfolio_risks)
import numpy_financial as npf
from datetime import datetime
# import yfinance as yf

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

def calculate_cagr(beginning_value, ending_value, years):
    """
    Calculate the compound annual growth rate (CAGR) of an investment.

    Parameters:
    beginning_value: float - The beginning value of the investment
    ending_value: float - The ending value of the investment

    Returns:
    float - The compound annual growth rate (CAGR) of the investment
    """
    return (ending_value / beginning_value) ** (1/years) - 1

def calculate_cagr_from_cash_flows(cash_flows):
    """
    Calculate the compound annual growth rate (CAGR) of an investment given a list of cash flows.

    Parameters:
    cash_flows: list - A list of cash flows for the investment

    Returns:
    float - The compound annual growth rate (CAGR) of the investment
    """
    beginning_value = cash_flows[0]
    ending_value = cash_flows[-1]
    years = len(cash_flows) - 1
    return calculate_cagr(beginning_value, ending_value, years)

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

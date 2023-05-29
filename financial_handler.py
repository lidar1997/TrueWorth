import requests
import json

import Buffet_methods


INCOME_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/financials/income-statement"
CASH_FLOW_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement"
BALANCE_SHEET_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement"
MARKET_CAP_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/market-capitalization"
DCF_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/discounted-cash-flow/"

YEARS_FOR_AVG = 3


def get_json_from_url(url):
    financial_data = requests.get(url)
    return json.loads(financial_data.text)


def calculate_growth_rate(owner_earnings_list):
    """
    Calculates the growth rate as a 10Y avg in YEARS_FOR_AVG-periods
    :param owner_earnings_list: list of past owner earnings (as defined by Warren Buffet)
    :return: the growth rate
    """
    if len(owner_earnings_list) < 2 * YEARS_FOR_AVG:
        raise IndexError("Not enough years to calculate avg growth rate\n")

    cur_avg = sum(owner_earnings_list[:YEARS_FOR_AVG]) / YEARS_FOR_AVG
    old_avg = sum(owner_earnings_list[-YEARS_FOR_AVG:]) / YEARS_FOR_AVG
    growth = cur_avg / old_avg
    growth_period = len(owner_earnings_list) - YEARS_FOR_AVG

    return growth ** (1/growth_period) - 1


def calculate_working_capital(current_year_balance_sheet, previous_year_balance_sheet):
    """
    Calculates the change in working capital
    :param current_year_balance_sheet: the balance sheet from last year
    :param previous_year_balance_sheet: the balance sheet from the current year
    :return: the change in working cap
    """
    current_assets = float(current_year_balance_sheet["Total assets"])
    current_liabilities = float(current_year_balance_sheet["Total liabilities"])
    working_capital = current_assets - current_liabilities

    previous_current_assets = float(previous_year_balance_sheet["Total assets"])
    previous_current_liabilities = float(previous_year_balance_sheet["Total liabilities"])
    previous_working_capital = previous_current_assets - previous_current_liabilities

    return working_capital - previous_working_capital


def get_financial_data(ticker, api_key, num_of_years):
    """
    returns the financial data required by the program
    :param ticker: stock to get the data for
    :param api_key: key for financialmodelingprep.com API
    :param num_of_years: to calculate the data for
    :return: owner_earnings_list - list of owner earnings as presented by Warren Buffet
             growth_rate - 10Y avg growth rate
             market_cap - company's market capacity
             financial_message - message for the data logger
    """
    operating_income_list = []
    d_and_a_list = []
    capEx_list = []
    working_cap_list = []
    owner_earnings_list = []
    total_debt_list = []

    income_data = get_json_from_url(INCOME_STATEMENT_URL + f"/{ticker}?apikey={api_key}")
    cash_flow_data = get_json_from_url(CASH_FLOW_STATEMENT_URL + f"/{ticker}?apikey={api_key}")
    balance_data = get_json_from_url(BALANCE_SHEET_STATEMENT_URL + f"/{ticker}?apikey={api_key}")
    cap_data = get_json_from_url(MARKET_CAP_STATEMENT_URL + f"/{ticker}?apikey={api_key}")
    market_cap = cap_data[0]["marketCap"]
    free_cash_flow = cash_flow_data["financials"][0]["Free Cash Flow"]

    income_type = "Operating Income"
    if float(income_data["financials"][0][income_type]) == 0:
        income_type = "Net Income"

    for i in range(num_of_years):
        try:
            operating_income_list.append(float(income_data["financials"][i][income_type]))
            d_and_a_list.append(float(cash_flow_data["financials"][i]["Depreciation & Amortization"]))
            capEx_list.append(float(cash_flow_data["financials"][i]["Capital Expenditure"]))
            working_cap_list.append(
                float(calculate_working_capital(balance_data["financials"][i], balance_data["financials"][i+1])))
            total_debt_list.append(balance_data["financials"][i]["Total debt"])

            owner_earnings_list.append(Buffet_methods.owner_earnings_per_share(operating_income_list[i],
                                                                               d_and_a_list[i],
                                                                               capEx_list[i],
                                                                               working_cap_list[i]))

        except Exception as exc:
            with open("logs.txt", 'a') as logs:
                logs.write(f"Stock: {ticker}\nAn exception happened: {exc}\n")
                logs.write(
                    f"last report was {i - 1} years ago. Growth rate will be calculated based on {i - 1} years\n\n")
            break

    growth_rate = calculate_growth_rate(owner_earnings_list)

    financial_message = (f"Average growth rate: {growth_rate}"
                         f"\nAnnual {income_type}: {operating_income_list}"
                         f"\nAnnual Depreciation & Amortization: {d_and_a_list}"
                         f"\nAnnual Capital Expenditure: {capEx_list}"
                         f"\nAnnual changes in working capital: {working_cap_list}"
                         f"\nTotal debt: {total_debt_list}"
                         f"\nFree cash flow: {free_cash_flow}"
                         f"\n\nCalculated annual owner earnings: {owner_earnings_list}"
                         f"\nMarket capacity: {market_cap}\n")

    return owner_earnings_list, growth_rate, market_cap, financial_message


def get_price_and_dcf(ticker, key):
    """
    gets the dfc result for the stock from the API
    :param ticker: stock's ticker for the API
    :param key: API key
    :return: today's date, current stock price and dcf per share
    """
    dcf_data = get_json_from_url(DCF_STATEMENT_URL + f"{ticker}?apikey={key}")[0]
    date = dcf_data["date"]
    price = float(dcf_data["Stock Price"])
    dcf_per_share = float(dcf_data["dcf"])
    return date, price, dcf_per_share


def get_manual_financial_data():
    """
    for foreign (non-US country) companies, must set data manually.
    :returns same as get_financial_data
    """
    owner_earnings_list = []

    # todo: fill those values with your company's data for manual use
    net_income = []
    dep_am = []
    capEx = []
    working_cap_changes = []
    market_cap = 0
    # end of todo

    for i in range(len(net_income)):
        owner_earnings_list.append(Buffet_methods.owner_earnings_per_share(net_income[i], dep_am[i],
                                                                           capEx[i], working_cap_changes[i]))

    growth_rate = calculate_growth_rate(owner_earnings_list)

    financial_message = (f"Average growth rate: {growth_rate}"
                         f"\nAnnual net income: {net_income}"
                         f"\nAnnual Depreciation & Amortization: {dep_am}"
                         f"\nAnnual Capital Expenditure: {capEx}"
                         f"\nAnnual changes in working capital: {working_cap_changes}"
                         f"\nCalculated annual owner earnings: {owner_earnings_list}"
                         f"\nMarket capacity: {market_cap}\n")

    return owner_earnings_list, growth_rate, market_cap, financial_message


def market_cap_to_intrinsic_value(market_cap, intrinsic_val):
    return market_cap / intrinsic_val

# TrueWorth
TrueWorth is a tool designed to help understand the true worth of a publicly traded company.

The tool employs Warren Buffett's method to determine a stock's intrinsic value, using the discounted cash flow method. If the intrinsic value is below the company's market cap, it is considered 'undervalued'.

**** UPDATE ****
right now the manual financial data is off, only US stocks are valid

============ HOW TO USE ============

1. get your API key from https://site.financialmodelingprep.com/developer. Note that if you choose the free edition you can use it only on US stocks, or use is_foreign_stock=true and insert your own data in financial_handler.get_manual_financial_data()
2. put your key in a new file called 'key_holder.txt' - make sure its in a single line and with no other characters!
3. run from your favorite IDE or terminal using this syntax: <stock_ticker> <num_of_years> <is_foreign_stock> where 
    ticker: str - the symbol of the desired stock
    num_of_years: int - the number of years to get the financial data from
    is_foreign_stock: bool - marker to use the manual inserted data


====================================

**** IMPORTANT ****

Please note that TrueWorth is a tool intended to assist in gaining a better understanding of a company's value. Any results obtained from this program should not be considered as advice for any kind of stock operation.

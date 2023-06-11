# TrueWorth
TrueWorth is a tool designed to help understand the true worth of a publicly traded company.

The tool employs Warren Buffett's method to determine a stock's intrinsic value, using the discounted cash flow method. If the intrinsic value is below the company's market cap, it is considered 'undervalued'.


============ HOW TO USE ============

1. Get your API key from https://site.financialmodelingprep.com/developer. Note that if you choose the free edition you can use it only on US stocks, or follow section 4 for foreign stocks.
2. Put your key in a new file called 'key_holder.txt' - make sure its in a single line and with no other characters!
3. Run from your favorite IDE or terminal, and fill the relevant fields in the GUI
    
4. How to run the algo for foreign stocks:
    4.1 Create a file under <project_name>\foreignStocks\<stock_ticker>.txt
    4.2 Fill the information in the file in the following format: - line 1 is the annual operating income, with ',' as delimeter only - no spaces!
                                                                  - line 2 is the same but for the annual depreciation & amortization
                                                                  - line 3 is the same but for the annual capEx
                                                                  - line 4 is the same but for the annual working cap change
                                                                  - line 5 is the market cap
    4.3 Run the app following section 3. using is_foreign_stock=true (the checkbox in the GUI)


====================================

**** IMPORTANT ****

Please note that TrueWorth is a tool intended to assist in gaining a better understanding of a company's value. Any results obtained from this program should not be considered as advice for any kind of stock operation.

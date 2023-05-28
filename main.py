import os
import sys
import tkinter as tk
from tkinter import messagebox

import Buffet_methods
import financial_handler as fh


KEY = "0ef11b1f00199ee665a2504f19b26fdb"
# KEY = "d361b8d1b456597441e62d6c884eef78"
BUFFET_DISCOUNT_RATE = 0.1


def main(ticker, num_of_years, use_manual_data):
    """
    main function of the program
    :param ticker: str - the symbol of the desired stock
    :param num_of_years: int - the number of years to get the financial data from
    :param use_manual_data: marker to use the manual inserted data
    """
    if use_manual_data:
        owner_earnings_list, growth_rate, market_cap, financial_message = fh.get_manual_financial_data()
        date = "28/5/2023"  # todo: CHANGE daily!
        api_response = "\n\n"

    else:
        owner_earnings_list, growth_rate, market_cap, financial_message = \
            fh.get_financial_data(ticker, KEY, num_of_years)
        date, share_price, dcf_per_share = fh.get_price_and_dcf(ticker, KEY)
        api_response = f"\nStock's price to APIs discounted cash flow: {share_price / dcf_per_share}\n\n"

    current_owner_earning = owner_earnings_list[0]

    if growth_rate < 0.01:
        print(f"Stock {ticker} has average annual growth rate of {growth_rate}, don't buy it!")
        return

    # if 10y avg growth is above 25%, assume 15% growth
    if growth_rate > 0.25:
        growth_rate = 0.15
        lower_growth_rate = 0.07
    else:
        # assume that growth rate will decline by half from 10y avg
        growth_rate /= 2
        lower_growth_rate = min(0.05, growth_rate)

    used_growth_rate_str = f"Used growth rate: {growth_rate}\n"

    intrinsic_val = Buffet_methods.intrinsic_value(current_owner_earning, growth_rate, lower_growth_rate,
                                                   BUFFET_DISCOUNT_RATE)

    response = f"Stock: {ticker}\nDate: {date}\nStock's market cap to intrinsic val ratio by Buffet: " \
               f"{fh.market_cap_to_intrinsic_value(market_cap, intrinsic_val)}" + api_response

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Buffet's Method", response)

    # write results
    if not os.path.exists("StocksReports"):
        os.mkdir("StocksReports")
    with open(f"StocksReports\\{ticker}_data.txt", 'w') as f:
        f.write(response + used_growth_rate_str + financial_message +
                f"Intrinsic val by Buffet: {intrinsic_val}\n\n")


if __name__ == "__main__":
    try:
        t = str.upper(sys.argv[1])
        number_of_years = int(sys.argv[2])
        is_foreign_stock = sys.argv[3].lower() in ("1", "true", "yes", "y")
        main(t, number_of_years, is_foreign_stock)

    except (TypeError, IndexError) as bad_args:
        print("Error: program's correct usage is: <stock_ticker> <num_of_years> <is_foreign_stock>")
        raise

    except Exception as e:
        try:
            print(e)
            with open("logs.txt", 'a') as r:
                r.write("An exception happened: " + str(e))
                r.write("\n\n")
            raise  # for debugging
        except IOError as ioe:
            print("*** ERROR ***")
            print(str(ioe))

import os
from datetime import date

import Buffet_methods
import financial_handler as fh


BUFFET_DISCOUNT_RATE = 0.1


def get_key():
    """
    get the key from key_holder.txt file
    """
    try:
        with open("key_holder.txt", 'r') as key_file:
            return key_file.readlines()[0].strip()
    except IOError:
        raise IOError("Error: can't read the key from key_holder.txt. make sure it exists!")


class Model:

    def __init__(self):
        self.key = get_key()

    def run(self, ticker, num_of_years, use_manual_data):
        """
        main function of the program
        :param ticker: str - the symbol of the desired stock
        :param num_of_years: int - the number of years to get the financial data from
        :param use_manual_data: marker to use the manual inserted data
        """
        if use_manual_data:
            owner_earnings_list, growth_rate, market_cap, financial_message = fh.get_manual_financial_data(ticker)

        else:
            owner_earnings_list, growth_rate, market_cap, financial_message = \
                fh.get_financial_data(ticker, self.key, num_of_years)

        today = date.today()

        current_owner_earning = owner_earnings_list[0]

        if growth_rate < 0.01:
            return f"Stock {ticker} has average annual growth rate of {growth_rate}, don't buy it!"

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

        response = f"Stock: {ticker}\nDate: {today}\nStock's market cap to intrinsic val ratio by Buffet:\n" \
                   f"{fh.market_cap_to_intrinsic_value(market_cap, intrinsic_val)}\n\n"

        # write results
        if not os.path.exists("StocksReports"):
            os.mkdir("StocksReports")
        with open(f"StocksReports\\{ticker}_data.txt", 'w') as f:
            f.write(response + used_growth_rate_str + financial_message +
                    f"Intrinsic val by Buffet: {intrinsic_val}\n\n")

        return response

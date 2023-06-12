
def calculate_owner_earnings(operating_income, depreciation_amortization, capital_exp, working_cap_changes):
    """
    Calculates the owner earnings per share (OEPS) of a company using online financial data according to
    Warren Buffet's method.

    Parameters:
    :param operating_income - company's operating income for that year
    :param depreciation_amortization depreciation and amortization
    :param capital_exp - company's capital expenditure
    :param working_cap_changes - changes in working cap

    :return The owner earnings per share of the company
    """

    return operating_income + depreciation_amortization + working_cap_changes + capital_exp


def intrinsic_value(owner_earnings, growth_rate, lower_future_growth_rate, discount_rate):
    """
    Calculates the intrinsic value of a company using the formula outlined in "The Warren Buffet Way" by
    Robert G. Hagstrom.
    :param owner_earnings: The company's current owner earnings (NOT per share)
    :param growth_rate: The company's projected annual growth rate (in percentage)
    :param lower_future_growth_rate: the company's lower est. future growth rate
    :param discount_rate: The discount rate used to calculate the present value of future cash flows (in percentage)

    :return: The intrinsic value of the company
    """

    discount_value = (1 - discount_rate)

    last_year_free_cash_flow = owner_earnings
    future_discounted_cash_flow_sum = 0
    for i in range(1, 11):
        last_year_free_cash_flow *= (1 + growth_rate)
        future_discounted_cash_flow_sum += (last_year_free_cash_flow * (discount_value**i))

    eleventh_year_cash_flow = last_year_free_cash_flow * (1 + lower_future_growth_rate)
    discounted_cash_flow = eleventh_year_cash_flow / (discount_rate - lower_future_growth_rate)
    last_cash_flow = discounted_cash_flow * discount_value**10

    return last_cash_flow + future_discounted_cash_flow_sum


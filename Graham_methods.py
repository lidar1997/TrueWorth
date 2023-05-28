# TODO: edit properly!


def graham_model(owner_earnings, growth_rate, current_bond_yield):
    """
    The idea behind the Graham Number is that a stock is considered undervalued if
    its price is less than the Graham Number, and overvalued if its price is greater
    than the Graham Number. Therefore, by using this formula, an investor can identify
    undervalued stocks that have a margin of safety, which is the difference between
    the stock's intrinsic value and its market price.

    :param owner_earnings: The company's current owner earnings (NOT per share)
    :param growth_rate: The company's projected annual growth rate (in percentage)
    :param current_bond_yield: the current yield from AA bonds
    :return graham number for the company (for all shares, not per share)
    """

    graham_number = owner_earnings * (8.5 + 2 * growth_rate) * 4.4 / current_bond_yield
    return graham_number

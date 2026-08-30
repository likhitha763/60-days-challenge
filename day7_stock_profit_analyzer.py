"""
Stock Profit Analyzer
----------------------
Given a list of daily stock prices, find the maximum profit achievable
from a single buy followed by a single sell (buy must happen before sell).

Approach: one pass, O(n) time, O(1) space.
Track the lowest price seen so far; at each day, check the profit if we
sold today having bought at that lowest price. Keep the best.

This is deliberately NOT the O(n^2) brute-force (try every buy/sell pair)
since the task explicitly calls out "optimization" as the learning goal.
"""


def max_profit(prices: list[float]) -> dict:
    """
    Returns a dict with:
      - max_profit: the best possible profit (0 if no profitable trade exists)
      - buy_day: index of the optimal day to buy (None if no profit possible)
      - sell_day: index of the optimal day to sell (None if no profit possible)
    """
    if len(prices) < 2:
        return {"max_profit": 0, "buy_day": None, "sell_day": None}

    min_price = prices[0]
    min_price_day = 0
    best_profit = 0
    best_buy_day = None
    best_sell_day = None

    for day in range(1, len(prices)):
        price = prices[day]
        profit_if_sold_today = price - min_price

        if profit_if_sold_today > best_profit:
            best_profit = profit_if_sold_today
            best_buy_day = min_price_day
            best_sell_day = day

        if price < min_price:
            min_price = price
            min_price_day = day

    return {
        "max_profit": round(best_profit, 2),
        "buy_day": best_buy_day,
        "sell_day": best_sell_day,
    }


def demo():
    prices = [7, 1, 5, 3, 6, 4]
    result = max_profit(prices)
    print(f"Prices: {prices}")
    print(f"Max profit: {result['max_profit']}")
    if result["buy_day"] is not None:
        print(f"Buy on day {result['buy_day']} (price={prices[result['buy_day']]}), "
              f"sell on day {result['sell_day']} (price={prices[result['sell_day']]})")
    else:
        print("No profitable trade possible (prices only decrease).")


if __name__ == "__main__":
    demo()
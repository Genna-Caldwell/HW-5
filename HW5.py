import json

# Load prices from a file, rounding each to 2 decimals
def load_prices(filepath):
    prices = []
    with open(filepath, "r") as f:
        for line in f:
            try:
                # Convert each line to float and round to 2 decimals
                price = round(float(line.strip()), 2)
                prices.append(price)
            except ValueError:
                continue
    return prices

# Mean reversion trading strategy logic
def meanReversionStrategy(prices):
    print("\nMean Reversion Strategy Output:")
    final_profit = 0
    first_buy = None
    buy_price = None
    trade_profits = []
    for i in range(5, len(prices)):
        current_price = prices[i]
        avg_price = sum(prices[i-5:i]) / 5
        # Buy logic if the price is sufficiently lower than the average
        if current_price < avg_price * 0.98:
            if buy_price is None:
                buy_price = current_price
                if first_buy is None:
                    first_buy = buy_price
                print("buying at:", round(buy_price, 2))
        # Sell logic if the price is sufficiently higher than the average
        elif current_price > avg_price * 1.02 and buy_price is not None:
            profit = round(current_price - buy_price, 2)
            final_profit += profit
            trade_profits.append(profit)
            print("selling at:", round(current_price, 2))
            print("trade profit:", profit)
            buy_price = None
    # Calculate final profit percentage
    if first_buy is not None and first_buy > 0:
        final_profit_percentage = round((final_profit / first_buy) * 100, 2)
    else:
        final_profit_percentage = 0.0
    print("\nTotal profit:", round(final_profit, 2))
    if first_buy is not None:
        print("First buy:", round(first_buy, 2))
    else:
        print("First buy: N/A")
    print("Percent return:", final_profit_percentage, "%")
    return final_profit, final_profit_percentage

# Simple moving average trading strategy logic
def simpleMovingAverageStrategy(prices):
    print("\nSimple Moving Average Strategy Output:")
    final_profit = 0
    first_buy = None
    buy_price = None
    trade_profits = []
    for i in range(5, len(prices)):
        current_price = prices[i]
        avg_price = sum(prices[i-5:i]) / 5
        # Buy logic if price above average
        if current_price > avg_price:
            if buy_price is None:
                buy_price = current_price
                if first_buy is None:
                    first_buy = buy_price
                print("buying at:", round(buy_price, 2))
        # Sell logic if price below average
        elif current_price < avg_price and buy_price is not None:
            profit = round(current_price - buy_price, 2)
            final_profit += profit
            trade_profits.append(profit)
            print("selling at:", round(current_price, 2))
            print("trade profit:", profit)
            buy_price = None
    # Calculate final profit percentage
    if first_buy is not None and first_buy > 0:
        final_profit_percentage = round((final_profit / first_buy) * 100, 2)
    else:
        final_profit_percentage = 0.0
    print("\nTotal profit:", round(final_profit, 2))
    if first_buy is not None:
        print("First buy:", round(first_buy, 2))
    else:
        print("First buy: N/A")
    print("Percent return:", final_profit_percentage, "%")
    return final_profit, final_profit_percentage

# Save results dictionary to results.json file
def saveResults(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

# Define tickers and file paths
tickers = ["AAPL", "ADBE", "AMZN", "BA", "DAL", "GOOG", "LHX", "LMT", "META", "NOC"]
filepaths = [
    "/workspaces/HW-5/AAPL.txt",
    "/workspaces/HW-5/ADBE.txt",
    "/workspaces/HW-5/AMZN.txt",
    "/workspaces/HW-5/BA.txt",
    "/workspaces/HW-5/DAL.txt",
    "/workspaces/HW-5/GOOG.txt",
    "/workspaces/HW-5/LHX.txt",
    "/workspaces/HW-5/LMT.txt",
    "/workspaces/HW-5/META.txt",
    "/workspaces/HW-5/NOC.txt"
]

results = {}

# Loop through each ticker file, run both strategies, and save results
for ticker, path in zip(tickers, filepaths):
    prices = load_prices(path)
    results[ticker + "_prices"] = prices

    print("="*60)
    print(ticker, "Results")
    print("="*60)

    # Mean Reversion
    mr_profit, mr_return = meanReversionStrategy(prices)
    results[ticker + "_mr_profit"] = mr_profit
    results[ticker + "_mr_returns"] = mr_return

    # Simple MA
    sma_profit, sma_return = simpleMovingAverageStrategy(prices)
    results[ticker + "_sma_profit"] = sma_profit
    results[ticker + "_sma_returns"] = sma_return

# Save all results to results.json
saveResults(results)
print("\nAll results saved to results.json.")

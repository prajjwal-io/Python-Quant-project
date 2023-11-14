import pandas as pd
import numpy as np

def calculate_features(stock_data):
  """Calculates the features used to identify oversold and overbought stocks.

  Args:
    stock_data: A Pandas DataFrame containing the stock data.

  Returns:
    A Pandas DataFrame containing the features for the stock.
  """

  features = pd.DataFrame()

  # Calculate the Price-to-Moving Average Ratio (PMAR)
  features["PMAR"] = stock_data["Close"] / stock_data["Close"].rolling(window=20).mean()

  # Calculate the Bollinger Bands Ratio
  upper_band = stock_data["Close"].rolling(window=20).mean() + 2 * stock_data["Close"].rolling(window=20).std()
  lower_band = stock_data["Close"].rolling(window=20).mean() - 2 * stock_data["Close"].rolling(window=20).std()
  features["Bollinger Bands Ratio"] = (stock_data["Close"] - lower_band) / (upper_band - lower_band)

  # Calculate the Relative Strength Index (RSI)
  changes = stock_data["Close"].diff()
  gains = changes[changes > 0]
  losses = abs(changes[changes < 0])
  features["RSI"] = gains.sum() / (gains.sum() + losses.sum())

  # Calculate the Moving Average Convergence Divergence (MACD)
  fast_ema = stock_data["Close"].ewm(span=12, min_periods=10).mean()
  slow_ema = stock_data["Close"].ewm(span=26, min_periods=20).mean()
  macd = fast_ema - slow_ema
  signal_ema = macd.ewm(span=9, min_periods=8).mean()
  features["MACD"] = macd - signal_ema

  # Calculate the Percentage Change from 20-day Low
  twenty_day_low = stock_data["Close"].rolling(window=20).min()
  features["Percentage Change from 20-day Low"] = (stock_data["Close"] - twenty_day_low) / twenty_day_low

  return features

def select_stocks(features):
  """Selects the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low.

  Args:
    features: A Pandas DataFrame containing the features for the stocks.

  Returns:
    A list of the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low.
  """

  # Sort the stocks by the features
  sorted_stocks = features.sort_values(by=["PMAR", "Bollinger Bands Ratio", "Percentage Change from 20-day Low"], ascending=True)

  # Select the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low
  selected_stocks = sorted_stocks.index[:10]

  return selected_stocks

def rebalance_portfolio(portfolio, selected_stocks):
  """Rebalances the portfolio to hold a long position of 100 shares of each stock in the selected_stocks list.

  Args:
    portfolio: A Pandas Series containing the current portfolio holdings.
    selected_stocks: A list of the stocks to hold in the portfolio.

  Returns:
    A Pandas Series containing the rebalanced portfolio holdings.
  """

  # Calculate the number of shares to buy and sell for each stock
  buy_orders = pd.Series(index=selected_stocks, data=100).astype(np.int16)
  sell_orders = portfolio[~portfolio.index.isin(selected_stocks)]

  # Left join the buy_orders and sell_orders Series to get the chunk Series
  chunk = buy_orders.merge(sell_orders, how="left", on="Symbol", fill_value=0)

  # Normalize the portfolio holdings to ensure that they sum to 1
  chunk = chunk / chunk.sum()

  return chunk


import pandas as pd

def prepare_stocks_data(csi500_file, all_stocks_data_file):
  """Prepares the stocks data for backtesting.

  Args:
    csi500_file: The path to the CSI 500 CSV file.
    all_stocks_data_file: The path to the all stocks data CSV file.

  Returns:
    A Pandas DataFrame containing the prepared stocks data.
  """

  # Read the CSI 500 CSV file.
  csi500 = pd.read_csv(csi500_file)

  # Read the all stocks data CSV file.
  all_stocks_data = pd.read_csv(all_stocks_data_file)

  # Merge the two DataFrames on the 'code' column.
  all_stocks_data = pd.merge(all_stocks_data, csi500, on='code')

  # Convert the 'date' column to a datetime format.
  all_stocks_data.index = pd.to_datetime(all_stocks_data['date'])

  # Select only the 'time', 'english_code', and 'close' columns.
  stocks_data = all_stocks_data[['time', 'english_code', 'close']]

  # Rename the 'english_code' column to 'Symbol'.
  stocks_data = stocks_data.rename(columns={'english_code': 'Symbol'})

  return stocks_data


def main():
  """Backtests the mean-reverting strategy."""

  # Prepare the stocks data
  stocks_data = prepare_stocks_data("csi500.csv", "all_stock_data.csv")
  # Calculate the features for each stock
  features = stocks_data.groupby("Symbol").apply(calculate_features)

  # Initialize the portfolio
  portfolio = pd.Series(index=stocks_data["Symbol"], data=0)
    # Get the list of all symbols in the features DataFrame.
  symbols = features.index.get_level_values("Symbol")
  dates = features.index.get_level_values("date")


  for symbol in symbols:
    for date in dates:
        # Select the stocks to hold in the portfolio
        selected_stocks = select_stocks(features.loc[symbol , date])
        print(selected_stocks)

        # Rebalance the portfolio
        portfolio = rebalance_portfolio(portfolio, selected_stocks)

        # Calculate the portfolio returns
        portfolio_returns = portfolio.pct_change()

  # Calculate the cumulative returns of the portfolio
  cumulative_returns = (1 + portfolio_returns).cumprod() - 1

  # Print the cumulative returns of the portfolio
  print(cumulative_returns)

if __name__ == "__main__":
  main()


"""The code is a mean-reverting strategy that selects the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low. The strategy then rebalances the portfolio to hold a long position of 100 shares of each stock in the selected_stocks list.

What measures can be taken to improve the code?
There are a few measures that can be taken to improve the code:

Use a more sophisticated stock selection algorithm: The current stock selection algorithm is very simple. It simply selects the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low. A more sophisticated algorithm could use other factors, such as technical indicators, fundamental data, or machine learning, to select stocks.

Use a more sophisticated portfolio rebalancing algorithm: The current portfolio rebalancing algorithm is also very simple. It simply rebalances the portfolio to hold a long position of 100 shares of each stock in the selected_stocks list. A more sophisticated algorithm could consider factors such as the risk-adjusted returns of the stocks in the portfolio and the transaction costs associated with rebalancing the portfolio.

Optimize the hyperparameters of the strategy: The strategy has a number of hyperparameters, such as the number of stocks to select and the rebalancing frequency. These hyperparameters can be optimized to improve the performance of the strategy."""
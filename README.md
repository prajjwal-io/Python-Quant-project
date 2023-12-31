# Python-Quant-project
## Mean-Reverting Strategy

This code implements a mean-reverting strategy for backtesting on stock data. The strategy works by selecting the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low. The strategy then rebalances the portfolio to hold a long position of 100 shares of each stock in the selected_stocks list.

**Strategy:**

1. Calculate the features for each stock:
    * PMAR
    * Bollinger Bands Ratio
    * Relative Strength Index (RSI)
    * Moving Average Convergence Divergence (MACD)
    * Percentage Change from 20-day Low
2. Select the 10 stocks with the lowest PMAR, Bollinger Bands Ratio, and Percentage Change from 20-day Low.
3. Rebalance the portfolio to hold a long position of 100 shares of each stock in the selected_stocks list.

4. Current update - As there are larger than 500 stocks which results in memory allocation error further approach can involve using backtrader and zipline for backtesting.

**Usage:**

To use the code, you will need to provide the following two files:

* `csi500.csv`: A CSV file containing the CSI 500 index data. - Use indexStockData.py to download
* `all_stocks_data.csv`: A CSV file containing all of the stock data for the stocks in the CSI 500 index. - Use allStockData.py to download (Files was alrger than 25 mb hence can't be uploaded) 
drive link : https://drive.google.com/file/d/1Jz2W0XUfza11TKh4-7ULd8tlUg6RoArn/view?usp=sharing

Once you have downloaded these two files, you can run the code by following these steps:

1. Install the required Python dependencies:

```python
pip install pandas numpy

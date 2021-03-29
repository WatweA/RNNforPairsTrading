# Project Proposal - DS4400
## Pairwise Stock Prediction
##### Team - Krasnonosenkikh, Daniel and Watwe, Aaditya


## Problem Description
We’re hoping to replicate a pair-wise long-short equity strategy for a basket of stocks traded on the NASDAQ and NYSE. This strategy entails finding closely correlated equities, and categorizing whether the first equity in the pair will outperform the other in the future day/week/month. The returns from this strategy are lower than buy-and-hold but the direction (up or down) of the market as a whole will not influence our returns. Based on the predicted future return ratio from our model, we will take a long position in the pair’s first asset and a short position in the other, if the future ratio is greater than 1. If the ratio is less than 1 we simply flip these positions. Thus all of the return we earn from the model will be based on the effectiveness of the model we select in predicting the ratio between the selected assets.


## Dataset
https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs
Full historical daily price and volume data for all US-based stocks and ETFs trading on the NYSE, NASDAQ, and NYSE MKT. The dataset shows Date, Open, High, Low, and Close prices for each stock, as well as Volume and OpenInt across 8539 total stocks and ETFs.

We can alternatively use the Google Finance API https://pypi.org/project/googlefinance/ to get all relevant data, for a list of assets (i.e. members of the S&P 500 or members of the Russell 2000). This way, we can focus our search on fewer companies and ensure that we have more recent data. 


## Approach and Methodology
Our approach is loosely inspired by this article from Investopedia:
https://www.investopedia.com/articles/trading/04/090804.asp

1. Find approximately 20 equity pairs:
   1. Get the average price each day by calculating the mean of open, high, low, and close prices, then calculate daily returns (daily % change) from this average price.
   2. Using daily returns, find closely correlated pairs by calculating Pearson’s correlation coefficient across the dataset of assets. We may choose to narrow down the search to assets which fall in the same industry and market cap. 
   3. Optional: We can also use an autoregressive model to tell if pairs have the same seasonality. Then find Pearson’s correlation coefficient between the seasonalities of the two assets.
      1. https://en.wikipedia.org/wiki/Autoregressive_model
2. Create feature columns for each selected pair with the following metrics (two columns for each metric, one for each asset):
   1. Volume and daily return (percent change) columns for both assets. The periodicity of our returns are to be decided, and depends on the trends we find in the data. Most likely, we will choose to use daily returns, but weekly and monthly time-spans may be more viable.
   2. Volatility calculated using OHLC for both assets. We may choose to include multiple volatility metrics (i.e. rolling 2-week standard deviation, rolling 1-month return range, implied volatility, etc.) .
   3. Next-day return predictions using a GARCH model on the daily return of each asset.
   4. 3 momentum indicators using 1-week, 1-month, and 1-quarter look-back windows.
3. Create one target column for each pair:
   1. Divide the daily return of the first asset at time, t + 1, by the other asset’s return at time, t + 1. This gives up the next day’s return ratio, our target for regression.
4. For each pair, create a model which can predict our target variable. The models we hope to use are RNNs (recurrent neural networks), SVM (support-vector machines), Bayesian regression, and random forest regression. We can use multiple linear regression and polynomial regression as a benchmark.
5. Profit.


## Metrics and Model Evaluation
1. We can evaluate our model by using R2 and RMSE between the model's predicted ratio and true future return ratio between the pairs. Then we will have approximately 20 values, and can take the mean across all 20.
2. We can convert the regression values into bucketed classes (i.e. buckets with limits 0-0.7, 0.7-0.95, 0.95-1.05, 1.05-1.3, 1.3+). Then using a confusion matrix, we will see the model’s tendencies, and whether there is a high presence of false positives or false negatives.
3. Finally, we will calculate the returns by converting the predicted ratio to long/short signals, and multiply these signals by true future return. This will calculate the model’s returns, which we can compare to the USD yield rate as a benchmark. We can also calculate sharpe ratio and drawdowns for these model returns, comparing them to the USD yield rate.


## References and Resources
Kaggle dataset of compiled stock prices found on google.com. 
* Source: https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs
* Similar projects on this Kaggle dataset can be viewed here: https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/code 
Data-scraping introduction for financial data using Python
* https://www.learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/
Pairs-Trading Article from Investopedia
* https://www.investopedia.com/terms/p/pairstrade.asp
Pairs Trading: Performance of a Relative-Value Arbitrage Rule
* https://doi.org/10.1093/rfs/hhj020 

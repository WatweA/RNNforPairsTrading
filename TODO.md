# Project TODO
Continue building as more tasks arise

### Data Collection
- [X] Scrape all data for assets in `data/info/tickers.txt` into pandas pickles in `data/raw/*.zip`:
  - [X] scrape data only for tickers which have values for both 1999-01-04 and 2021-03-01
  - [X] calculate an average of OHLC price column
  - [X] calcuate a rate-of-change column for the averaged daily price (one day look-back)
  - [X] save the DataFrame as a pickle in `data/raw/<ticker>.zip`

### Exploratory Data Analysis
- [X] calculate and save pairwise corellations:
  - [X] read all data from the rate-of-change columns in `data/raw/*.zip` into one DataFrame
  - [X] calculate all pairwise corellations between columns
  - [X] generate a dictionary with a key for each ticker and a list of its 5 most closely corellated tickers with the Pearson-r coefficient
    - i.e. this would look like the following JSON when saved to a file:
      ```JSON
      { "someTicker1": {
          "otherTicker1": 0.972143,
          "otherTicker2": 0.928475,
          "otherTicker3": 0.919085,
          "otherTicker4": 0.907268,
          "otherTicker5": 0.893265
        }, ...
      }
      ```
  - [X] place these pairs into `data/info/corellations.json`
- [X] select pairs:
  - [X] read pairs from `data/info/corellations.json`
  - [X] find at least 25 unique pairs and save them to `data/info/pairs.json` pairs as keys, correlations as values

### Feature Generation
- [X] implement geometric Brownian motion simulation for the ratio of returns
- [ ] implement ARIMA with 5 autoregressive look-backs and 1 differencing step on log returns as a feature column
- [ ] save all generated dataframes in `data/processed/[ticker_a]-[ticker_b].zip`

### Benchmark Models
- [X] implement methods to find cumulative returns of a returns DataFrame, and to get the columns' annualized returns
- [ ] implement methods to take predicted return ratios and real return ratios and evaluate them as:
  - [ ] regression, with RMSE/MSE and Pearson r
  - [ ] classification, with accuracy, confusion matrix, and F1-scores for positive/negative classifications
    - [ ] IMPORTANT: fix the bucket sizes for regression prediction into classes
  - [X] financial, with sharpe ratio, excess return, and annualized return
- [ ] generate method to apply sci-kit learn model over a rolling window given features and a target column
  - parameters: training window size, testing window size
- [ ] for all pairs in `pairs.json`, train and evaluate the following models:
  - use following random seed: 81734
  - [ ] linear regression (Elastic Net) with L1 and/or L2 regularization
  - [ ] SVM regression, with cross validation to find the optimal regression parameter, and a linear kernel
  - [ ] random forest regression
  - [ ] ADABoost and GradientBoostingRegressor
  - [ ] Feed-forward NN
  - [ ] RNN (top of stack)
  - [ ] save all predicted dataframes in `data/pred/[ticker_a]-[ticker_b].zip`
    - columns: all feature columns, true return column, one predicted return column for each model

### Data Visualizations
- [ ] heat map sorted by industry then by ticker name
- [ ] threshold plot for cumulative returns comparing true vs. predicted
- [ ] ROC Curve: 1 for each pair, includes line for all models
- [ ] optional: Tableau dashboard if time allows


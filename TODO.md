# Project TODO
Continue building as more tasks arise

### Data Collection
- [X] Scrape all data for assets in `data/info/tickers.txt` into pandas pickles in `data/raw/*.zip`:
  - [X] scrape data only for tickers which have values for both 1999-01-04 and 2021-03-01
  - [X] calculate an average of OHLC price column
  - [X] calcuate a rate-of-change column for the averaged daily price (one day look-back)
  - [X] save the DataFrame as a pickle in `data/raw/<ticker>.zip`

### Exploratory Data Analysis
- [ ] calculate and save pairwise corellations:
  - [X] read all data from the rate-of-change columns in `data/raw/*.zip` into one DataFrame
  - [ ] calculate all pairwise corellations between columns
  - [ ] generate a dictionary with a key for each ticker and a list of its 5 most closely corellated tickers with the Pearson-r coefficient
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
  - [ ] place these pairs into `data/info/corellations.json`
- [ ] select pairs:
  - [ ] read pairs from `data/info/corellations.json`
  - [ ] find at least 25 unique pairs and save them to `data/info/pairs.txt` (one pair per line, comma separated)

### Benchmark Models
- [ ] ...

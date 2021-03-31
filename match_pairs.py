from typing import Dict, Tuple
import glob
import pandas as pd
import json


# get the names of all tickers from data/raw
tickers = sorted([ticker[9:-4] for ticker in glob.glob("data/raw/*.zip")])

daily_returns = pd.DataFrame(index=pd.date_range(start="1999-01-05", end="2021-03-01", 
                                                 freq=pd.tseries.offsets.BDay(), name="Date"))  # business dates
for ticker in tickers:
    df = pd.read_pickle("data/raw/" + ticker + ".zip")  # needs pickle5 compression (python 3.8)
    daily_returns[ticker] = df["Log Return"].fillna(method='ffill')

print("daily log returns dataframe:")
print(daily_returns)

# get pairwise Pearson correlations for all tickers
corr = daily_returns.corr(method="pearson")


def top_n_pairs(n: int=5) -> Dict[str, Dict[str, float]]:
    """
    extracts the top n correlations for each ticker in `tickers` using Pearson r values from `corr`
    """
    pairs_dict: Dict[str, Dict[str, float]]=dict()
    for ticker in tickers:
        top_n = corr.sort_values(by=[ticker])[ticker][(-1 - n):-1] # exclude itself
        assert top_n.name == ticker
        pairs_dict[ticker] = top_n.to_dict({})
    
    return pairs_dict


top_5_corr = top_n_pairs()
# Save as a JSON
top_5_corr_JSON = json.dumps(top_5_corr, sort_keys=False, indent=4, separators=(',', ': '))
save_path = "data/info/corellations.json"
open(save_path,"w").write(top_5_corr_JSON)
print(top_5_corr)


def match_tickers(corr_dict: Dict[str, Dict[str, float]], min_corr=0, debug=False):
    """
    Use a non-optimal variant of the Gale-Shapley algorithm to generate matches from the given 
    correlations dictionary. This algorithm will iterate a maximum of 100 times over all pairs in 
    the dictionary, and override matches when a better alternate match arises.
    A dictionary of matched ticker pairs and their correlations will be returned.
    """
    all_tickers: Set[str] = set()
    all_pairs: Dict[Tuple[str, str], float] = dict()
    # iterate over all pairs, and add the SORTED tuple of tickers with their correlations
    # sorting ensures (A, B) and (B, A) will not both be added
    for ticker_a, ticker_a_dict in corr_dict.items():
        for ticker_b, a_b_corr in ticker_a_dict.items():
            # for ticker pairs above the minimum corr, add to the set and dict
            if min_corr <= a_b_corr:
                all_tickers.add(ticker_a); all_tickers.add(ticker_b)
                all_pairs[tuple(sorted([ticker_a, ticker_b]))] = a_b_corr
    
    # use a modified non-optimal version of Gale-Shapley to find the matchings
    unmatched: Dict[str, bool] = {ticker: True for ticker in all_tickers}
    matches: Dict[str, str] = dict()  # use dict instead of list of sets for speed
    i = 0  # terminate at 100 iterations
    while any([unmatched_i for unmatched_i in unmatched.values()]) and i < 100:
        if debug:
            num_matched = sum([1 for unmatched_i in unmatched.values() if not unmatched_i])
            print(f"Iteration: {i}, number matched: {num_matched}")
        for (ticker_a, ticker_b), a_b_corr in all_pairs.items():
            if unmatched[ticker_a] and unmatched[ticker_b]:
                unmatched[ticker_a] = False; unmatched[ticker_b] = False
                matches[ticker_a] = ticker_b; matches[ticker_b] = ticker_a
            else:
                a_pair = tuple(sorted([ticker_a, matches.get(ticker_a, "")]))
                b_pair = tuple(sorted([ticker_b, matches.get(ticker_b, "")]))
                a_corr = all_pairs.get(a_pair, 0.0)
                b_corr = all_pairs.get(b_pair, 0.0)
                # if tickers a and b are better corellated than their current matches
                if a_corr < a_b_corr and b_corr < a_b_corr:
                    if debug: 
                        print(f"pair: {(ticker_a, ticker_b)} better than {a_pair} and {b_pair}")
                    # remove the current matches (checking if they exist)
                    ticker_a_match = matches.get(ticker_a, "")
                    ticker_b_match = matches.get(ticker_b, "")
                    if ticker_a_match != "": 
                        unmatched[ticker_a_match] = True
                        del matches[ticker_a_match]
                    if ticker_b_match != "": 
                        unmatched[ticker_b_match] = True
                        del matches[ticker_b_match]
                    
                    # match ticker_a and ticker_b
                    unmatched[ticker_a] = False; unmatched[ticker_b] = False
                    matches[ticker_a] = ticker_b; matches[ticker_b] = ticker_a
        i += 1
    
    matched_pairs: Dict[Tuple[str, str], float] = {
        tuple(sorted([ticker_a, ticker_b])): all_pairs.get(tuple(sorted([ticker_a, ticker_b])))
        for (ticker_a, ticker_b) in matches.items()
    }
    return matched_pairs


# get the matched tickers for all with correlation coefficients above 0.75
matched_tickers = match_tickers(top_5_corr, min_corr=0.75)
# tuple to str representation for keys, save as JSON
matched_tickers_JSON = json.dumps(
    {str(k): v for k,v in matched_tickers.items()}, 
    sort_keys=False, indent=4, separators=(',', ': '))
save_path = "data/info/pairs.json"
open(save_path,"w").write(matched_tickers_JSON)
print(matched_tickers)


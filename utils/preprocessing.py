import pandas as pd
import pandas_market_calendars as mcal
from utils.models import GeometricBrownianMotion
from statsmodels.tsa.arima.model import ARIMA


def generate_pair_data(df_A: pd.DataFrame,
                       df_B: pd.DataFrame,
                       start: str,
                       end: str,
                       ) -> pd.DataFrame:
    """
    Generates the DataFrame of training features using raw price, volume, and daily return data for two pairs of
    correlated assets. The target column will be named "Return Diff (t+1)", and will be the difference in next-day
    returns of the first asset minus the second.

    :param df_A: price, volume, and return data for the first asset in the pair
    :param df_B: price, volume, and return data for the second asset in the pair
    :param start: the start date, given as a "YYYY-MM-DD" string
    :param end: the ending date, given as a "YYYY-MM-DD" string
    :return: the DataFrame of features and the target column
    """
    # initialize dataframe with trading day indices
    dates = mcal.get_calendar('NYSE').schedule(start_date=start, end_date=end).index
    pair_df = pd.DataFrame(index=dates)  # trading dates

    # establish the rolling windows for both tickers in the pair
    rolling_1w_A = df_A.rolling(10)
    rolling_1m_A = df_A.rolling(21)
    rolling_3m_A = df_A.rolling(63)
    # rolling_6m_A = df_A.rolling(126)
    # rolling_1y_A = df_A.rolling(252)
    rolling_1w_B = df_B.rolling(10)
    rolling_1m_B = df_B.rolling(21)
    rolling_3m_B = df_B.rolling(63)
    # rolling_6m_B = df_B.rolling(126)
    # rolling_1y_B = df_B.rolling(252)

    # add the rolling volatility ratios
    pair_df["1W Std."] = rolling_1w_A["Log Return"].std(ddof=0) / rolling_1w_B["Log Return"].std(ddof=0)
    pair_df["1M Std."] = rolling_1m_A["Log Return"].std(ddof=0) / rolling_1m_B["Log Return"].std(ddof=0)
    pair_df["3M Std."] = rolling_3m_A["Log Return"].std(ddof=0) / rolling_3m_B["Log Return"].std(ddof=0)
    # pair_df["6M Std."] = rolling_6m_A["Log Return"].std(ddof=0) / rolling_6m_B["Log Return"].std(ddof=0)
    # pair_df["1Y Std."] = rolling_1y_A["Log Return"].std(ddof=0) / rolling_1y_B["Log Return"].std(ddof=0)

    # add the rolling mean return differences
    pair_df["1D Simple Ret."] = df_A["Simple Return"] - df_B["Simple Return"]
    pair_df["1D Ret."] = df_A["Log Return"] - df_B["Log Return"]
    pair_df["1W Ret."] = rolling_1w_A["Log Return"].mean() - rolling_1w_B["Log Return"].mean()
    pair_df["1M Ret."] = rolling_1m_A["Log Return"].mean() - rolling_1m_B["Log Return"].mean()
    pair_df["3M Ret."] = rolling_3m_A["Log Return"].mean() - rolling_3m_B["Log Return"].mean()
    # pair_df["6M Ret."] = rolling_6m_A["Log Return"].mean() - rolling_6m_B["Log Return"].mean()
    # pair_df["1Y Ret."] = rolling_1y_A["Log Return"].mean() - rolling_1y_B["Log Return"].mean()

    # add the volume columns adjusted for USD as a ratio
    pair_df["1D Vol Ratio"] = (df_A["Adj Close"] * df_A["Volume"]) / (df_B["Adj Close"] * df_B["Volume"])
    pair_df["1W Vol Ratio"] = ((rolling_1w_A["Adj Close"].mean() * rolling_1w_A["Volume"].mean()) /
                               (rolling_1w_B["Adj Close"].mean() * rolling_1w_B["Volume"].mean()))
    pair_df["1M Vol Ratio"] = ((rolling_1m_A["Adj Close"].mean() * rolling_1m_A["Volume"].mean()) /
                               (rolling_1m_B["Adj Close"].mean() * rolling_1m_B["Volume"].mean()))
    pair_df["3M Vol Ratio"] = ((rolling_3m_A["Adj Close"].mean() * rolling_3m_A["Volume"].mean()) /
                               (rolling_3m_B["Adj Close"].mean() * rolling_3m_B["Volume"].mean()))
    # pair_df["6M Vol Ratio"] = ((rolling_6m_A["Adj Close"].mean() * rolling_6m_A["Volume"].mean()) /
    #                            (rolling_6m_B["Adj Close"].mean() * rolling_6m_B["Volume"].mean()))
    # pair_df["1Y Vol Ratio"] = ((rolling_1y_A["Adj Close"].mean() * rolling_1y_A["Volume"].mean()) /
    #                            (rolling_1y_B["Adj Close"].mean() * rolling_1y_B["Volume"].mean()))

    # add the columns for projected geometric Brownian motion return using the rolling momentum and volatility values
    pair_df["1D GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(100) - 1
                               for mu, sigma in zip(list(pair_df["1D Ret."]), list(pair_df["1W Std."]))]
    pair_df["1W GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(100) - 1
                               for mu, sigma in zip(list(pair_df["1W Ret."]), list(pair_df["1W Std."]))]
    pair_df["1M GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(100) - 1
                               for mu, sigma in zip(list(pair_df["1M Ret."]), list(pair_df["1M Std."]))]
    pair_df["3M GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(100) - 1
                               for mu, sigma in zip(list(pair_df["3M Ret."]), list(pair_df["3M Std."]))]
    # pair_df["6M GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(10) - 1
    #                            for mu, sigma in zip(list(pair_df["6M Ret."]), list(pair_df["6M Std."]))]
    # pair_df["1Y GBM Proj."] = [GeometricBrownianMotion(1, mu, sigma).simulate_average_sT(10) - 1
    #                            for mu, sigma in zip(list(pair_df["1Y Ret."]), list(pair_df["1Y Std."]))]

    # this is the target column: when diff > 1, return is greater for pair[0], else return is greater for pair[1]
    pair_df["Return Diff (t+1)"] = df_A["Simple Return"] - df_B["Simple Return"]
    pair_df["Return Diff (t+1)"].shift(-1)  # shift so the return ratio at day t+1 moves to day t

    pair_df.fillna(0, inplace=True)
    return pair_df

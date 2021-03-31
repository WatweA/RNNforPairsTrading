from typing import Tuple, Dict, Optional

import numpy as np
import pandas as pd


def to_signal(predicted_returns: np.ndarray,
              signal_dict: Dict[Tuple[Optional[float], Optional[float]], float] = None
              ) -> np.ndarray:
    """
    Generate a list of signals given a list of returns and a dictionary of range mappings to returns

    :param predicted_returns: a list of return values
    :param signal_dict: a dictionary of range mappings to signals, where a range is a tuple representing the inclusive
        minimum and the exclusive maximum. A None is used where there is no minimum or maximum value for the range. (
        i.e. for the range of all numbers greater than 0.05 one would say (0.05, None)
    :return: a list of signals
    """
    if signal_dict is None:
        signal_dict = {
            (None, -0.0150): -1.00,
            (-0.0150, -0.0100): -0.75,
            (-0.0100, -0.0075): -0.50,
            (-0.0075, -0.0050): -0.25,
            (-0.0050, -0.0025): -0.10,
            (-0.0025, 0.0025): 0.00,
            (0.0025, 0.0050): 0.10,
            (0.0050, 0.0075): 0.25,
            (0.0075, 0.0100): 0.50,
            (0.0100, 0.0150): 0.75,
            (0.0150, None): 1.00
        }
    signals = []
    for i in range(len(predicted_returns)):
        predicted_return = predicted_returns[i]
        signal = 1
        for (range_min, range_max), range_signal in signal_dict.items():
            if (range_min is None or range_min <= predicted_return) and \
                    (range_max is None or predicted_return < range_max):
                signal = range_signal
        signals.append(signal)
    return np.ndarray(signals)


def adjusted_returns(signals: np.ndarray,
                     returns_a: np.ndarray,
                     returns_b: np.ndarray
                     ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates the adjusted returns for two returns series with a given signal for the pairwise returns.
    This method will apply the signal to returns_a and apply the negative signal to returns_b, and return both
    adjusted return arrays in a tuple.

    :param signals: the signals used to scale the first returns relative to the second
    :param returns_a: the first returns series in the pair
    :param returns_b: the second returns series in the pair
    :return: a tuple of the adjusted returns series
    """
    adjusted_a = []
    adjusted_b = []
    for i, signal in enumerate(signals):
        adjusted_a.append(returns_a[1] * signal)
        adjusted_b.append(returns_b[1] * -1 * signal)
    return np.array(adjusted_a), np.array(adjusted_b)


def annualized_return(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate an return the annualized return for all columns in the returns DataFrame

    :param returns_df: the DataFrame of returns
    :return: a series of annualized returns for each column
    """
    cumprod_df = returns_df
    cumprod_df.fillna(0, inplace=True)
    cumprod_df.iloc[0, :] += 1
    return cumprod_df.cumprod(axis=0)

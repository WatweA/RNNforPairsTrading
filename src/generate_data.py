#!/usr/bin/python

import pandas as pd
import json

pairs = {eval(k): v for k,v in dict(json.loads(open("data/info/pairs.json", "r").read())).items()}

pair = ('ADX', 'TY')
df_A = pd.read_pickle("data/raw/" + pair[0] + ".zip")  # needs pickle5 compression (python 3.8)
df_B = pd.read_pickle("data/raw/" + pair[1] + ".zip")  # needs pickle5 compression (python 3.8)

pair_df = generate_pair_data(df_A, df_B, "1999-01-01", "2021-03-01")

pair_df.loc["2000-01-01":, :]

for pair in pairs.keys():
    df_A = pd.read_pickle("data/raw/" + pair[0] + ".zip")  # needs pickle5 compression (python 3.8)
    df_B = pd.read_pickle("data/raw/" + pair[1] + ".zip")  # needs pickle5 compression (python 3.8)
    pair_df = generate_pair_data(df_A, df_B, "1999-01-01", "2021-03-01")
    pair_df.to_pickle(f"data/processed/{pair[0].upper()}-{pair[1].upper()}.zip")
    print(f"saved data/processed/{pair[0].upper()}-{pair[1].upper()}.zip")

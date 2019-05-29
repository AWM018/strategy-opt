# -*- coding: utf-8 -*-

"""Main module."""

import pandas as pd

def gen_HA(df : pd.DataFrame) -> pd.Series:
    ha = (df.close + df.open + df.high + df.low) / 4.
    return ha


def HA(df : pd.DataFrame) -> pd.DataFrame:
    df['heikin_ashi'] = gen_HA(df)
    return df


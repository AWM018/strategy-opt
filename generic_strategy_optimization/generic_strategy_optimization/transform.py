# -*- coding: utf-8 -*-

"""Main module."""

import pandas as pd
import numpy as np

def gen_HA(df : pd.DataFrame) -> pd.Series:
    ha = (df.close + df.open + df.high + df.low) / 4.
    return ha


def HA(df : pd.DataFrame) -> pd.DataFrame:
    df['heikin_ashi'] = gen_HA(df)
    return df


def downsample(df: pd.DataFrame, N: int, method: str = 'coarse') -> pd.DataFrame:
    assert method in ['fine', 'coarse']

    L = df.low.rolling(N).apply(min)
    H = df.high.rolling(N).apply(max)
    O = df.open.rolling(N).apply(lambda a: a[0])
    C = df.close.rolling(N).apply(lambda a: a[-1])
    V = df.volume.rolling(N).apply(sum)

    if method == 'coarse':
        ix = (len(df) + N - 1) % N
        rv = pd.DataFrame.from_items([
            #('ts', ts[ix::N]),
            ('low', L[ix::N]),
            ('high', H[ix::N]),
            ('open', O[ix::N]),
            ('close', C[ix::N]),
            ('volume', V[ix::N]),
        ]).dropna(axis=0)
        rv.index = df.index[(len(df) % N)::N]

        return rv
    elif method == 'fine':
        rv = [pd.DataFrame.from_items([
            #('ts', ts[ix::N]),
            ('low', L[ix::N]),
            ('high', H[ix::N]),
            ('open', O[ix::N]),
            ('close', C[ix::N]),
            ('volume', V[ix::N]),
        # the trick below is needed because except for the last dataframe in the tuple
        # the remaining N-1 ones will have the first row with NaNs. Here we have an 'if'
        # which allows us to drop the first conditionally for these.
        ]).iloc[(0 if ix == N - 1 else 1)::, :]
            for ix in range(0, N)]

        rv = pd.concat(rv).sort_index()
        rv.index = df.index[:-(N - 1)]

        return rv

# -*- coding: utf-8 -*-

"""Main module."""

import pandas as pd
import numpy as np

from .wallet import Wallet
from .Decimal import Dec, ZERO


def backtest(df: pd.DataFrame, signal: pd.Series, wallet: Wallet) -> Wallet:
    assert len(df) == len(signal)

    for price, command, timestamp in zip(df.close, signal, signal.index.values):

        if np.isnan(price) or np.isnan(command):
            continue

        command = Dec(min(max(command, -1), +1))
        price = Dec(price)

        if command == ZERO:
            pass
        elif command < ZERO:
            wallet.sell(price, -command, timestamp)
        elif command > ZERO:
            wallet.buy(price, command, timestamp)

    return wallet

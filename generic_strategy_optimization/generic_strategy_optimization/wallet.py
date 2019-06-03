# -*- coding: utf-8 -*-

import decimal
from .Decimal import *

HUNDRED = Dec('100')

import pandas as pd

class Wallet(object):
    def __init__(self,
            instrument: decimal.Decimal = ZERO,
            base: decimal.Decimal = ONE,
            base_limit: decimal.Decimal = ONE,
            fee: decimal.Decimal = Dec('0.1'),
            accumulate_excess: bool = True,
        ):
        self.instrument = Dec(instrument)
        self.base = Dec(base)
        self.base_limit = Dec(base_limit)
        self.fee = Dec(fee)
        self.accumulate_excess = bool(accumulate_excess)
        self.excess = ZERO

        self.history_ts = []
        self.history_base = []
        self.history_excess = []
        self.history_instrument = []


    def buy(self, price: decimal.Decimal, fraction: decimal.Decimal, ts: int):
        price = Dec(price)
        fraction = min(Dec(fraction), ONE)
        ts = int(ts)

        # selling currency
        if self.accumulate_excess:
            to_sell = min(self.base_limit, self.base) * fraction
        else:
            to_sell = self.base * fraction

        sold = (to_sell / price) / (ONE + self.fee / HUNDRED)
        self.instrument += sold
        self.base -= to_sell

        self.history_ts.append(ts)
        self.history_base.append(self.base)
        self.history_excess.append(self.excess)
        self.history_instrument.append(self.instrument)


    def sell(self, price: decimal.Decimal, fraction: decimal.Decimal, ts: int):
        pass


    @property
    def history(self):
        rv = pd.DataFrame.from_dict(
            {
                'ts': self.history_ts,
                'base': self.history_base,
                'excess': self.history_excess,
                'instrument': self.history_instrument,
            }
        ).set_index('ts')
        return rv


    @property
    def balance(self):
        return self.instrument, self.base, self.excess

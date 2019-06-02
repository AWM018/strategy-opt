# -*- coding: utf-8 -*-

import decimal
from .Decimal import *

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
        self.changes = None


    def buy(self, fraction: decimal.Decimal, ts: float):
        pass


    def sell(self, fraction: decimal.Decimal, ts: float):
        pass


    @property
    def history(self):
        return self.changes


    @property
    def balance(self):
        return self.instrument, self.base, self.excess

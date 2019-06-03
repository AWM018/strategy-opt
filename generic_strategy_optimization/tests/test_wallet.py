#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wallet` package."""

from generic_strategy_optimization.Decimal import *
from generic_strategy_optimization.wallet import Wallet

import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal
import pytest


FIVE = Dec('5.')


@pytest.fixture
def empty_wallet():
    rv = Wallet(instrument=ZERO, base=ONE, base_limit=ONE, fee=Dec('0.1'), accumulate_excess=True)
    return rv


def test_wallet_can_be_created(empty_wallet):
    pass


def test_initial_wallet_has_correct_state(empty_wallet):
    assert len(empty_wallet.history) == 0
    assert empty_wallet.balance == (ZERO, ONE, ZERO)


def test_can_buy_instrument_with_all_base(empty_wallet):

    empty_wallet.buy(price=FIVE, fraction=ONE, ts=1559512879)

    assert empty_wallet.balance == (Dec('0.2') / Dec('1.001') , ZERO, ZERO)
    assert_frame_equal(
        empty_wallet.history,
        pd.DataFrame.from_items([
            ['ts', [1559512879]],
            ['base', [ZERO]],
            ['excess', [ZERO]],
            ['instrument', [Dec('0.2') / Dec('1.001')]],
        ]).set_index('ts')
    )

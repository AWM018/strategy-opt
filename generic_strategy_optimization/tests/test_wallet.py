#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wallet` package."""

from generic_strategy_optimization.Decimal import *
from generic_strategy_optimization.wallet import Wallet

import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal
import pytest


QUARTER = Dec('0.25')
HALF = Dec('0.5')
FOUR = Dec('4.')
FIVE = Dec('5.')
SIX = Dec('6.')


@pytest.fixture
def empty_wallet():
    rv = Wallet(instrument=ZERO, base=ONE, base_limit=ONE, fee=Dec('0.1'), accumulate_excess=True)
    return rv


@pytest.fixture
def full_wallet():
    rv = Wallet(instrument=ONE, base=ZERO, base_limit=ONE, fee=Dec('0.1'), accumulate_excess=True)
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


def test_can_buy_instrument_with_some_base(empty_wallet):

    empty_wallet.buy(price=FIVE, fraction=HALF, ts=1559512879)

    assert empty_wallet.balance == (Dec('0.1') / Dec('1.001') , HALF, ZERO)
    assert_frame_equal(
        empty_wallet.history,
        pd.DataFrame.from_items([
            ['ts', [1559512879]],
            ['base', [HALF]],
            ['excess', [ZERO]],
            ['instrument', [Dec('0.1') / Dec('1.001')]],
        ]).set_index('ts')
    )


def test_can_buy_instrument_with_some_base_twice(empty_wallet):

    empty_wallet.buy(price=FIVE, fraction=HALF, ts=1559512879)
    empty_wallet.buy(price=FIVE, fraction=HALF, ts=1559513879)

    assert empty_wallet.balance == (Dec('0.1') / Dec('1.001') + Dec('0.05') / Dec('1.001'), QUARTER, ZERO)
    assert_frame_equal(
        empty_wallet.history,
        pd.DataFrame.from_items([
            ['ts', [1559512879, 1559513879]],
            ['base', [HALF, QUARTER]],
            ['excess', [ZERO, ZERO]],
            ['instrument', [Dec('0.1') / Dec('1.001'), Dec('0.1') / Dec('1.001') + Dec('0.05') / Dec('1.001')]],
        ]).set_index('ts')
    )


def test_buy_with_nothing_buys_nothing(full_wallet):

    full_wallet.buy(price=FIVE, fraction=HALF, ts=1559512879)

    assert full_wallet.balance == (ONE, ZERO, ZERO)
    assert_frame_equal(
        full_wallet.history,
        pd.DataFrame.from_items([
            ['ts', [1559512879]],
            ['base', [ZERO]],
            ['excess', [ZERO]],
            ['instrument', [ONE]],
        ]).set_index('ts')
    )


def __test_can_buy_instrument_with_some_base_and_then_sell_with_loss_with_no_excess_accumulated(empty_wallet):

    empty_wallet.buy(price=FIVE, fraction=HALF, ts=1559512879)
    print(empty_wallet.balance)
    empty_wallet.sell(price=FOUR, fraction=HALF, ts=1559513879)

    print(empty_wallet.balance)
    assert empty_wallet.balance == (Dec('0.1') / Dec('1.001') , HALF, ZERO)
    assert_frame_equal(
        empty_wallet.history,
        pd.DataFrame.from_items([
            ['ts', [1559512879]],
            ['base', [HALF]],
            ['excess', [ZERO]],
            ['instrument', [Dec('0.1') / Dec('1.001')]],
        ]).set_index('ts')
    )

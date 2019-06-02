#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wallet` package."""

from generic_strategy_optimization.Decimal import *
import pytest

from generic_strategy_optimization.wallet import Wallet


@pytest.fixture
def empty_wallet():
    rv = Wallet(instrument=ZERO, base=ONE, base_limit=ONE, fee=Dec('0.1'), accumulate_excess=True)
    return rv


def test_wallet_can_be_created(empty_wallet):
    pass


def test_initial_wallet_has_correct_state(empty_wallet):
    assert empty_wallet.history is None
    assert empty_wallet.balance == (ZERO, ONE, ZERO)


def test_can_buy_instrument_with_all_base(empty_wallet):

    empty_wallet.buy(ONE, 1559512879.)

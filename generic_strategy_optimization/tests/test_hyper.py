#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hyper` package."""

from generic_strategy_optimization.hyper import evaluate

from hyperopt import hp
import numpy as np
import pytest


@pytest.fixture
def linear_data():
    rv = np.linspace(-2, +2, num=123)
    return rv


def test_evaluate_finds_minimum(linear_data):

    def objective(data_gen, params):
        rv = np.sum((data_gen() - params['v'] + 3.14) ** 2)
        return rv

    rv = evaluate(
        objective=objective,
        data_gen=lambda: linear_data,
        space={'v': hp.uniform('v', -10, 10)},
        neval=250
        )

    v = rv['v']

    assert v > 3. and v < 3.5

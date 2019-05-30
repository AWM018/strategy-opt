#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `transform` package."""

import pytest
import pandas as pd
from pandas.testing import assert_series_equal

from generic_strategy_optimization.transform import HA, gen_HA


@pytest.fixture
def candles_5m_short():
    arr = [
            [1504927800,303.11,305.1,305.02,304.39,452.56688104],
            [1504928100,303.99,304.4,304.39,303.99,508.66859951],
            [1504928400,303.04,304.4,303.99,303.88,526.7675571],
          ]
    rv = pd.DataFrame(arr, columns=('ts', 'low', 'high', 'open', 'close', 'volume'))
    return rv


def test_HA_adds_heikin_ashi_column_to_dataframe(candles_5m_short):
    """Sample pytest test function with the pytest fixture as an argument."""

    df = HA(candles_5m_short)
    assert 'heikin_ashi' in df
    assert len(df) == len(candles_5m_short)
    assert_series_equal(df.heikin_ashi, pd.Series([304.405, 304.1925, 303.8275]), check_names=False)



#!/usr/bin/python3

"""
Display contiguous ranges in tick series
"""

import bz2
import json
import pandas as pd
import numpy as np


fname = "/repo/python-binance/examples/Binance_LTCUSDT_1m_1513135920000-1514764800000.json.bz2"
with bz2.open(fname, 'rt') as f:
    trades1 = json.loads(f.read())

fname = '/repo/python-binance/examples/Binance_LTCUSDT_1m_1514764800000-1546300800000.json.bz2'
with bz2.open(fname, 'rt') as f:
    trades2 = json.loads(f.read())

fname = '/repo/python-binance/examples/Binance_LTCUSDT_1m_1546300800000-1559001600000.json.bz2'
with bz2.open(fname, 'rt') as f:
    trades3 = json.loads(f.read())

trades1.extend(trades2[:-1])
trades1.extend(trades3)


fname = '/repo/python-binance/examples/Binance_LTCUSDT_1m_1513135920000-1559001600000.json.bz2'
with bz2.open(fname, 'wt') as f:
    f.write(json.dumps(trades1))

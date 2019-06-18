#!/usr/bin/python3

"""
Display contiguous ranges in tick series
"""

import bz2
import json
import pandas as pd
import numpy as np
import datetime


DIFF = 1 * 60 * 1000
do_split = True

fname = "/repo/python-binance/examples/Binance_LTCUSDT_1m_1513135920000-1514764800000.json.bz2"
fname = '/repo/python-binance/examples/Binance_LTCUSDT_1m_1514764800000-1546300800000.json.bz2'
fname = '/repo/python-binance/examples/Binance_LTCUSDT_1m_1546300800000-1559001600000.json.bz2'
fname = 'Binance_LTCUSDT_1m_1513135920000-1559001600000.json.bz2'

with bz2.open(fname, 'rt') as f:
    trades = json.loads(f.read())
    df = pd.DataFrame(trades, columns=['ts', 'open', 'high', 'low', 'close', 'volume', 'close_ts', 'quote_volume', 'ntrades', 'buy_base_volume', 'buy_quote_volume', '_'])
    df.drop(['close_ts', 'quote_volume', 'ntrades', 'buy_base_volume', 'buy_quote_volume', '_'], inplace=True, axis=1)


    epochs = df.ts.values

    # https://stackoverflow.com/questions/7352684/how-to-find-the-groups-of-consecutive-elements-from-an-array-in-numpy/7353335#7353335
    ranges = np.split(epochs, np.where(np.diff(epochs) != DIFF)[0] + 1)
    lengths = [0] + [len(r) for r in ranges]
    bounds = np.cumsum(lengths)

    print("Found {} ranges".format(len(ranges)))
    print("Bounds {}".format(bounds))

    lengths = [len(r) for r in ranges]
    assert(len(epochs) == sum(lengths))

    print("Top-N longest ranges {}".format(sorted(lengths, reverse=True)[:12]))

    if do_split:
        for begin in range(len(bounds) - 1):
            ts_begin = trades[bounds[begin]][0]
            ts_end = trades[bounds[begin + 1] - 1][0]

            dt_begin = datetime.datetime.utcfromtimestamp(ts_begin // 1000).isoformat()
            dt_end = datetime.datetime.utcfromtimestamp(ts_end // 1000).isoformat()
            ofname = 'out_{}-{}.json.bz2'.format(ts_begin, ts_end)
            print('{} -- {} {:>6d}  {}'.format(dt_begin, dt_end, bounds[begin + 1] - bounds[begin], ofname))

            with bz2.open(ofname, 'wt') as ofile:
                ofile.writelines(json.dumps(trades[bounds[begin]:bounds[begin + 1]]))

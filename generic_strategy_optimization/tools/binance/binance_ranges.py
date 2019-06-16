#!/usr/bin/python3

"""
Extract two longest ranges from ETH
"""



fname = "ETHUSD_05m_A_latest.log"
# Found 8 ranges
# Top-5 longest ranges [37121, 32040, 28169, 9148, 5734]


import numpy as np

df = np.loadtxt(fname, usecols=(1,2,3,4,5), delimiter=',')

epochs = df[:, 0]

# https://stackoverflow.com/questions/7352684/how-to-find-the-groups-of-consecutive-elements-from-an-array-in-numpy/7353335#7353335
ranges = np.split(epochs, np.where(np.diff(epochs) != 300)[0] + 1)

lengths = [0] + [len(r) for r in ranges]
bounds = np.cumsum(lengths)

print(bounds)

with open(fname, 'r') as f:
    ll = f.readlines()

    for begin in range(len(bounds) - 1):

        with open('eth{}.csv'.format(begin), 'w') as ofile:
            ofile.writelines(ll[bounds[begin]:bounds[begin + 1]])

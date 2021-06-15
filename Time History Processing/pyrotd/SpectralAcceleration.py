# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:57:22 2021

@author: Kite
"""


import os

import matplotlib.pyplot as plt
import numpy as np

import pyrotd
pyrotd.processes = 1

# Load the AT2 timeseries
fname = os.path.join(
    os.path.dirname(__file__), 'RSN1176_KOCAELI_YPT060.AT2')
    #os.path.dirname(__file__), 'RSN1176_KOCAELI_YPT150.AT2')
with open(fname) as fp:
    for _ in range(3):
        next(fp)
    line = next(fp)
    time_step = float(line[17:25])
    accels = np.array([p for l in fp for p in l.split()]).astype(float)

# Compute the acceleration response spectrum
osc_damping = 0.05
osc_freqs = np.logspace(-1, 2, 91)
resp_spec = pyrotd.calc_spec_accels(time_step, accels, osc_freqs, osc_damping)

for x in resp_spec:
    x[0] = 1 / x[0]
    
    print(x[0])

print(resp_spec)

# Create a plot!
fig, ax = plt.subplots()

ax.plot(resp_spec.osc_freq, resp_spec.spec_accel)

ax.set(
    xlabel='Period (sec)',
    xscale='linear',
    ylabel='5%-Damped Spectral Accel. (g)',
    yscale='linear', )
ax.grid()

plt.xlim([0, 10])

fig.tight_layout()
plt.show(fig)
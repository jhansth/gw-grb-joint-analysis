import numpy as np
import pandas as pd


def simulate_gw_events(n=50, t0=1.126e9):
    times = t0 + np.sort(np.random.uniform(0, 1e4, n))
    snr = np.random.normal(10, 2, n)
    ra = np.random.uniform(0, 2*np.pi, n)
    dec = np.random.uniform(-np.pi/2, np.pi/2, n)

    return pd.DataFrame({
        "time_gps": times,
        "snr": snr,
        "ra": ra,
        "dec": dec
    })

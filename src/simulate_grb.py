import numpy as np
import pandas as pd


def simulate_grb_events(n=20, t0=1.126e9):
    times = t0 + np.sort(np.random.uniform(0, 1e4, n))
    fluence = np.random.lognormal(-7, 0.5, n)
    ra = np.random.uniform(0, 2*np.pi, n)
    dec = np.random.uniform(-np.pi/2, np.pi/2, n)

    return pd.DataFrame({
        "time_gps": times,
        "fluence": fluence,
        "ra": ra,
        "dec": dec
    })

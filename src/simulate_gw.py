"""Simulate GW trigger events and write them to CSV.

Inputs:
- n: number of simulated GW events
- t0: starting GPS time in seconds

Outputs:
- data/simulated/gw_triggers.csv
"""

from pathlib import Path
import logging

import numpy as np
import pandas as pd


def simulate_gw_events(n=200, t0=1.126e9):
    """Simulate GW triggers with simple distributions.

    Args:
        n: number of simulated events.
        t0: GPS start time (seconds).

    Returns:
        DataFrame with columns: event_id, time_gps, snr, ra, dec.
        ra/dec are in radians and snr is dimensionless.
    """
    times = t0 + np.sort(np.random.uniform(0, 1e4, n))
    snr = np.random.normal(10, 2, n)
    ra = np.random.uniform(0, 2*np.pi, n)
    dec = np.random.uniform(-np.pi/2, np.pi/2, n)

    df = pd.DataFrame({
        "time_gps": times,
        "snr": snr,
        "ra": ra,
        "dec": dec
    })

    df.insert(0, "event_id", [f"GW{idx + 1:03d}" for idx in range(len(df))])
    return df


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    out_dir = Path("data/simulated")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "gw_triggers.csv"

    df = simulate_gw_events()
    df.to_csv(out_path, index=False)
    logging.info("Saved GW triggers to %s", out_path)


if __name__ == "__main__":
    main()

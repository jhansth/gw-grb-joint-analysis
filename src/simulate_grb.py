"""Simulate GRB trigger events and write them to CSV.

Inputs:
- n: number of simulated GRB events
- t0: starting GPS time in seconds

Outputs:
- data/simulated/grb_triggers.csv
"""

from pathlib import Path
import logging

import numpy as np
import pandas as pd

import config


def _offset_sky(ra, dec, sigma_rad, rng):
    """Offset sky positions by a small random angle (radians)."""
    if sigma_rad <= 0:
        return ra, dec, np.zeros_like(ra)

    # Rayleigh gives radial distance for 2D Gaussian offsets
    delta = rng.rayleigh(sigma_rad, size=ra.shape)
    phi = rng.uniform(0, 2 * np.pi, size=ra.shape)

    sin_dec0 = np.sin(dec)
    cos_dec0 = np.cos(dec)
    sin_delta = np.sin(delta)
    cos_delta = np.cos(delta)

    sin_dec = sin_dec0 * cos_delta + cos_dec0 * sin_delta * np.cos(phi)
    sin_dec = np.clip(sin_dec, -1.0, 1.0)
    dec_new = np.arcsin(sin_dec)

    y = np.sin(phi) * sin_delta * cos_dec0
    x = cos_delta - sin_dec0 * sin_dec
    ra_new = ra + np.arctan2(y, x)
    ra_new = np.mod(ra_new, 2 * np.pi)

    return ra_new, dec_new, delta


def simulate_grb_events(
    n=500,
    t0=1.126e9,
    gw_events=None,
    correlated_fraction=0.0,
    delay_mu=1.7,
    delay_sigma=0.5,
    sky_sigma_deg=2.0
):
    """Simulate GRB triggers with simple distributions.

    Args:
        n: number of simulated events.
        t0: GPS start time (seconds).

    If gw_events is provided, a fraction of GRBs are correlated to GW
    events with small time/sky offsets.

    Returns:
        DataFrame with columns: event_id, time_gps, fluence, ra, dec,
        plus optional diagnostic columns for correlated events.
    """
    rng = np.random.default_rng()
    sigma_rad = np.deg2rad(sky_sigma_deg)

    n_corr = 0
    if gw_events is not None and correlated_fraction > 0:
        n_corr = int(round(n * correlated_fraction))
        n_corr = min(n_corr, len(gw_events))

    n_uncorr = n - n_corr

    # Uncorrelated GRBs (background)
    uncorr_times = t0 + rng.uniform(0, 1e4, n_uncorr)
    uncorr_ra = rng.uniform(0, 2 * np.pi, n_uncorr)
    uncorr_dec = rng.uniform(-np.pi / 2, np.pi / 2, n_uncorr)

    corr_times = np.array([])
    corr_ra = np.array([])
    corr_dec = np.array([])
    corr_offsets = np.array([])
    parent_ids = []
    time_offsets = np.array([])

    if n_corr > 0:
        gw_sample = gw_events.sample(n=n_corr, replace=False, random_state=None)
        gw_ra = gw_sample["ra"].to_numpy()
        gw_dec = gw_sample["dec"].to_numpy()
        gw_time = gw_sample["time_gps"].to_numpy()

        time_offsets = rng.normal(delay_mu, delay_sigma, size=n_corr)
        corr_times = gw_time + time_offsets
        corr_ra, corr_dec, corr_offsets = _offset_sky(gw_ra, gw_dec, sigma_rad, rng)
        parent_ids = gw_sample["event_id"].tolist()

    # Combine
    times = np.concatenate([corr_times, uncorr_times])
    ra = np.concatenate([corr_ra, uncorr_ra])
    dec = np.concatenate([corr_dec, uncorr_dec])
    fluence = rng.lognormal(-7, 0.5, n)

    is_corr = np.array([True] * n_corr + [False] * n_uncorr)
    parent_ids = parent_ids + [""] * n_uncorr
    sky_offsets = np.concatenate([corr_offsets, np.full(n_uncorr, np.nan)])
    time_offsets = np.concatenate([time_offsets, np.full(n_uncorr, np.nan)])

    # Shuffle to avoid grouped ordering
    order = rng.permutation(n)
    times = times[order]
    ra = ra[order]
    dec = dec[order]
    fluence = fluence[order]
    is_corr = is_corr[order]
    parent_ids = [parent_ids[i] for i in order]
    sky_offsets = sky_offsets[order]
    time_offsets = time_offsets[order]

    df = pd.DataFrame({
        "time_gps": times,
        "fluence": fluence,
        "ra": ra,
        "dec": dec,
        "is_correlated": is_corr,
        "parent_gw_id": parent_ids,
        "time_offset_s": time_offsets,
        "sky_offset_rad": sky_offsets
    })

    df.insert(0, "event_id", [f"GRB{idx + 1:03d}" for idx in range(len(df))])
    return df


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    out_dir = Path("data/simulated")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "grb_triggers.csv"

    df = simulate_grb_events()
    df.to_csv(out_path, index=False)
    logging.info("Saved GRB triggers to %s", out_path)


if __name__ == "__main__":
    main()

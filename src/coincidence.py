"""Find GW-GRB coincidences and compute ranking statistics.

Inputs:
- data/simulated/gw_triggers.csv
- data/simulated/grb_triggers.csv

Outputs:
- data/results/coincident_events.csv
"""

from pathlib import Path
import logging

import numpy as np
import pandas as pd

from src import config


def angular_distance(ra1, dec1, ra2, dec2):
    """Great-circle angular separation (radians)."""
    return np.arccos(
        np.sin(dec1) * np.sin(dec2)
        + np.cos(dec1) * np.cos(dec2) * np.cos(ra1 - ra2)
    )


def normal_pdf(x, mu, sigma):
    """Normal PDF evaluated at x."""
    if sigma <= 0:
        return 0.0
    coeff = 1.0 / (sigma * np.sqrt(2.0 * np.pi))
    return float(coeff * np.exp(-0.5 * ((x - mu) / sigma) ** 2))


def lognormal_pdf(x, mu, sigma):
    """Log-normal PDF evaluated at x (x must be > 0)."""
    if sigma <= 0 or x <= 0:
        return 0.0
    coeff = 1.0 / (x * sigma * np.sqrt(2.0 * np.pi))
    return float(coeff * np.exp(-0.5 * ((np.log(x) - mu) / sigma) ** 2))


def overlap_kernel(delta, sigma):
    """Gaussian overlap kernel for time/sky separation."""
    if sigma <= 0:
        return 0.0
    return float(np.exp(-0.5 * (delta / sigma) ** 2))


def compute_rates(gw, grb):
    """Estimate per-second trigger rates from the simulated span."""
    if "time_gps" not in gw.columns or "time_gps" not in grb.columns:
        return 0.0, 0.0, 1.0

    times = np.concatenate([gw["time_gps"].to_numpy(), grb["time_gps"].to_numpy()])
    if len(times) < 2:
        return 0.0, 0.0, 1.0

    t_min = float(times.min())
    t_max = float(times.max())
    t_span = max(t_max - t_min, 1.0)

    r_gw = len(gw) / t_span
    r_grb = len(grb) / t_span
    return r_gw, r_grb, t_span


def find_coincidences(gw, grb, dt, domega):
    """Return a list of (gw_time, grb_time, angle_rad) coincidences."""
    coincidences = []

    for _, g in gw.iterrows():
        for _, r in grb.iterrows():
            if abs(g.time_gps - r.time_gps) < dt:
                ang = angular_distance(g.ra, g.dec, r.ra, r.dec)
                if ang < domega:
                    coincidences.append((g.time_gps, r.time_gps, ang))

    return coincidences


def build_coincidence_table(gw, grb, dt, domega):
    """Compute coincidence pairs and hypothesis-related likelihood proxies."""
    rows = []

    r_gw, r_grb, t_span = compute_rates(gw, grb)
    p_sky_noise = domega / (4.0 * np.pi)
    p_time_noise = dt / t_span

    for g in gw.itertuples(index=False):
        for r in grb.itertuples(index=False):
            delta_t = abs(g.time_gps - r.time_gps)
            if delta_t < dt:
                ang = angular_distance(g.ra, g.dec, r.ra, r.dec)
                if ang < domega:
                    snr = getattr(g, "snr", np.nan)
                    fluence = getattr(r, "fluence", np.nan)

                    i_t = overlap_kernel(delta_t, config.SIGMA_T)
                    i_omega = overlap_kernel(ang, config.SIGMA_OMEGA)
                    i_theta = i_t * i_omega

                    p_gw_signal = normal_pdf(snr, config.SNR_SIGNAL_MU, config.SNR_SIGNAL_SIGMA)
                    p_grb_signal = lognormal_pdf(fluence, config.FLUENCE_LOGNORM_MU, config.FLUENCE_LOGNORM_SIGMA)

                    p_d_hc = p_gw_signal * p_grb_signal * i_theta
                    p_d_hnn = (r_gw * dt) * (r_grb * dt) * p_sky_noise
                    p_d_hsn = p_gw_signal * (r_grb * dt) * p_sky_noise
                    p_d_hns = (r_gw * dt) * p_sky_noise * p_grb_signal
                    p_d_hss = p_gw_signal * p_grb_signal * p_time_noise * p_sky_noise

                    p_d_h0 = (
                        p_d_hnn * config.PRIOR_HNN
                        + p_d_hsn * config.PRIOR_HSN
                        + p_d_hns * config.PRIOR_HNS
                        + p_d_hss * config.PRIOR_HSS
                    )
                    p_d_h1 = p_d_hc * config.PRIOR_HC

                    if p_d_h0 <= 0:
                        rank_lambda = float("inf")
                        p_h0_d = 0.0
                        p_h1_d = 1.0
                    else:
                        rank_lambda = p_d_h1 / p_d_h0
                        p_h0_d = 1.0 / (1.0 + rank_lambda)
                        p_h1_d = rank_lambda / (1.0 + rank_lambda)

                    rows.append({
                        "gw_event_id": getattr(g, "event_id", ""),
                        "grb_event_id": getattr(r, "event_id", ""),
                        "gw_time": g.time_gps,
                        "grb_time": r.time_gps,
                        "delta_t": delta_t,
                        "angle_rad": ang,
                        "gw_snr": snr,
                        "grb_fluence": fluence,
                        "I_t": i_t,
                        "I_omega": i_omega,
                        "I_theta": i_theta,
                        "p_gw_signal": p_gw_signal,
                        "p_grb_signal": p_grb_signal,
                        "p_D_HC": p_d_hc,
                        "p_D_Hnn": p_d_hnn,
                        "p_D_Hsn": p_d_hsn,
                        "p_D_Hns": p_d_hns,
                        "p_D_Hss": p_d_hss,
                        "p_D_H0": p_d_h0,
                        "p_D_H1": p_d_h1,
                        "rank_lambda": rank_lambda,
                        "p_H0_D": p_h0_d,
                        "p_H1_D": p_h1_d
                    })

    columns = [
        "gw_event_id",
        "grb_event_id",
        "gw_time",
        "grb_time",
        "delta_t",
        "angle_rad",
        "gw_snr",
        "grb_fluence",
        "I_t",
        "I_omega",
        "I_theta",
        "p_gw_signal",
        "p_grb_signal",
        "p_D_HC",
        "p_D_Hnn",
        "p_D_Hsn",
        "p_D_Hns",
        "p_D_Hss",
        "p_D_H0",
        "p_D_H1",
        "rank_lambda",
        "p_H0_D",
        "p_H1_D"
    ]
    return pd.DataFrame(rows, columns=columns)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    gw_path = Path("data/simulated/gw_triggers.csv")
    grb_path = Path("data/simulated/grb_triggers.csv")
    out_path = Path("data/results/coincident_events.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    gw = pd.read_csv(gw_path)
    grb = pd.read_csv(grb_path)

    coincidences = build_coincidence_table(
        gw, grb, config.DELTA_T, config.DELTA_OMEGA
    )
    coincidences.to_csv(out_path, index=False)
    logging.info("Saved %s coincidences to %s", len(coincidences), out_path)


if __name__ == "__main__":
    main()

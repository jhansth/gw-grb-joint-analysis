"""One-command pipeline for simulation, coincidence, stats, and plots.

Inputs:
- command line flags (n-gw, n-grb, seed, t0)

Outputs:
- data/simulated/*.csv
- data/results/*.csv and *.txt
- figures/*.png
"""

import argparse
import logging
from pathlib import Path

import numpy as np

from src import config, plotting, analysis_plots
from src.simulate_gw import simulate_gw_events
from src.simulate_grb import simulate_grb_events
from src.coincidence import build_coincidence_table
from src.statistics import compute_summary_stats, write_summary


def parse_args():
    parser = argparse.ArgumentParser(description="Run the GW-GRB simulation pipeline.")
    parser.add_argument("--n-gw", type=int, default=100, help="Number of GW triggers")
    parser.add_argument("--n-grb", type=int, default=500, help="Number of GRB triggers")
    parser.add_argument("--t0", type=float, default=1.126e9, help="Start GPS time (seconds)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--skip-plots", action="store_true", help="Skip all plot generation")
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)

    data_sim = Path("data/simulated")
    data_res = Path("data/results")
    data_sim.mkdir(parents=True, exist_ok=True)
    data_res.mkdir(parents=True, exist_ok=True)

    gw = simulate_gw_events(n=args.n_gw, t0=args.t0)
    grb = simulate_grb_events(
        n=args.n_grb,
        t0=args.t0,
        gw_events=gw if config.ENABLE_CORRELATED_GRB else None,
        correlated_fraction=config.CORRELATED_GRB_FRACTION,
        delay_mu=config.GRB_DELAY_MU,
        delay_sigma=config.GRB_DELAY_SIGMA,
        sky_sigma_deg=config.GRB_SKY_SIGMA_DEG
    )

    gw_path = data_sim / "gw_triggers.csv"
    grb_path = data_sim / "grb_triggers.csv"
    gw.to_csv(gw_path, index=False)
    grb.to_csv(grb_path, index=False)
    logging.info("Saved simulated triggers to %s and %s", gw_path, grb_path)

    coincidences = build_coincidence_table(gw, grb, config.DELTA_T, config.DELTA_OMEGA)
    coinc_path = data_res / "coincident_events.csv"
    coincidences.to_csv(coinc_path, index=False)
    logging.info("Saved %s coincidences to %s", len(coincidences), coinc_path)

    stats = compute_summary_stats(gw, grb, coincidences)
    summary_path = data_res / "summary_stats.txt"
    write_summary(summary_path, stats)
    logging.info("Saved summary stats to %s", summary_path)

    if not args.skip_plots:
        plotting.main()
        analysis_plots.main()

    logging.info("Pipeline complete.")


if __name__ == "__main__":
    main()

"""Generate analysis plots from coincidence results.

Inputs:
- data/results/coincident_events.csv

Outputs:
- figures/*.png (histograms and scatter plots)
"""

from pathlib import Path
import logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FIG_DIR = Path("figures")
COINC_PATH = Path("data/results/coincident_events.csv")


def save_empty(title, out_path):
    """Save a placeholder figure when no coincidences exist."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.5, 0.5, "No coincidences to plot", ha="center", va="center")
    ax.set_axis_off()
    ax.set_title(title)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_hist(series, title, xlabel, out_path, bins=30):
    """Save a histogram from a pandas Series."""
    values = series.dropna().to_numpy()
    if len(values) == 0:
        save_empty(title, out_path)
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(values, bins=bins, color="#2C7FB8", edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("count")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    FIG_DIR.mkdir(exist_ok=True)

    if not COINC_PATH.exists():
        logging.info("No coincident_events.csv found. Run the pipeline first.")
        return

    df = pd.read_csv(COINC_PATH)
    if df.empty:
        save_empty("No coincidences", FIG_DIR / "analysis_no_coincidences.png")
        logging.info("No coincidences to plot.")
        return

    if "delta_t" in df.columns:
        save_hist(
            df["delta_t"],
            "Coincidence time offsets",
            "Delta t (s)",
            FIG_DIR / "analysis_delta_t_hist.png"
        )

    if "angle_rad" in df.columns:
        save_hist(
            df["angle_rad"],
            "Coincidence angular separation",
            "Angle (rad)",
            FIG_DIR / "analysis_angle_hist.png"
        )

    if "rank_lambda" in df.columns:
        lambda_vals = df["rank_lambda"].replace([np.inf, -np.inf], np.nan)
        lambda_vals = lambda_vals[lambda_vals > 0]
        log_lambda = np.log10(lambda_vals)
        save_hist(
            log_lambda,
            "Ranking statistic (log10 Lambda)",
            "log10(Lambda)",
            FIG_DIR / "analysis_rank_lambda_hist.png"
        )

    if "p_H1_D" in df.columns:
        save_hist(
            df["p_H1_D"].clip(0, 1),
            "Signal posterior probability",
            "p(H1 | D)",
            FIG_DIR / "analysis_pH1_hist.png",
            bins=20
        )

    if "delta_t" in df.columns and "angle_rad" in df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(df["delta_t"], df["angle_rad"], s=12, alpha=0.7)
        ax.set_title("Delta t vs angular separation")
        ax.set_xlabel("Delta t (s)")
        ax.set_ylabel("Angle (rad)")
        fig.tight_layout()
        fig.savefig(FIG_DIR / "analysis_dt_vs_angle.png", dpi=200, bbox_inches="tight")
        plt.close(fig)

    logging.info("Saved analysis plots to %s", FIG_DIR.resolve())


if __name__ == "__main__":
    main()

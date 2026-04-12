"""Generate sky localization plots from simulated triggers.

Inputs:
- data/simulated/gw_triggers.csv
- data/simulated/grb_triggers.csv

Outputs:
- figures/*.png (sky maps and point plots)
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import healpy as hp
import matplotlib.pyplot as plt

import config

DEFAULT_NSIDE = 64
FIG_DIR = Path("figures")
COINC_PATH = Path("data/results/coincident_events.csv")


def load_triggers(path):
    """Load trigger CSV and return DataFrame plus HEALPix theta/phi."""
    df = pd.read_csv(path)
    ra = df["ra"].to_numpy()
    dec = df["dec"].to_numpy()

    if np.nanmax(np.abs(ra)) > 2 * np.pi or np.nanmax(np.abs(dec)) > np.pi / 2:
        ra = np.deg2rad(ra)
        dec = np.deg2rad(dec)

    theta = np.pi / 2 - dec
    phi = ra
    return df, theta, phi


def density_map(theta, phi, nside=DEFAULT_NSIDE):
    """Return a simple count map on a HEALPix grid."""
    m = np.zeros(hp.nside2npix(nside))
    pix = hp.ang2pix(nside, theta, phi)
    for p in pix:
        m[p] += 1
    return m


def normalize_map(m):
    """Normalize a map to sum to 1."""
    total = np.sum(m)
    if total <= 0:
        return m
    return m / total


def smooth_map(m, fwhm_deg):
    """Smooth a HEALPix map with a Gaussian kernel."""
    if fwhm_deg <= 0:
        return m
    return hp.smoothing(m, fwhm=np.deg2rad(fwhm_deg), verbose=False)


def theta_phi_from_ra_dec(ra, dec):
    theta = np.pi / 2 - dec
    phi = ra
    return theta, phi


def save_overlap_with_coincidences(overlap_map, gw_df, grb_df, outpath, title):
    """Overlay coincidence pairs on top of an overlap sky map."""
    if not COINC_PATH.exists():
        return

    coinc = pd.read_csv(COINC_PATH)
    if coinc.empty:
        return

    gw_lookup = gw_df.set_index("event_id")
    grb_lookup = grb_df.set_index("event_id")

    gw_ra = gw_lookup.loc[coinc["gw_event_id"], "ra"].to_numpy()
    gw_dec = gw_lookup.loc[coinc["gw_event_id"], "dec"].to_numpy()
    grb_ra = grb_lookup.loc[coinc["grb_event_id"], "ra"].to_numpy()
    grb_dec = grb_lookup.loc[coinc["grb_event_id"], "dec"].to_numpy()

    gw_theta, gw_phi = theta_phi_from_ra_dec(gw_ra, gw_dec)
    grb_theta, grb_phi = theta_phi_from_ra_dec(grb_ra, grb_dec)

    # Quick plausibility summary: overlap values at coincidence points
    gw_pix = hp.ang2pix(DEFAULT_NSIDE, gw_theta, gw_phi)
    grb_pix = hp.ang2pix(DEFAULT_NSIDE, grb_theta, grb_phi)
    overlap_vals = np.concatenate([overlap_map[gw_pix], overlap_map[grb_pix]])
    if overlap_vals.size > 0:
        logging.info(
            "Mean overlap at coincidence points: %.4g",
            float(np.mean(overlap_vals))
        )

    hp.mollview(overlap_map, title=title, unit="probability")
    hp.projscatter(gw_theta, gw_phi, s=35, c="red", marker="o", label="GW coincidences")
    hp.projscatter(grb_theta, grb_phi, s=35, c="blue", marker="x", label="GRB coincidences")
    hp.graticule()

    ax = plt.gca()
    ax.legend(loc="lower left")
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close()


def save_mollview(m, title, outpath, unit="counts"):
    """Save a mollview of a HEALPix map."""
    hp.mollview(m, title=title, unit=unit)
    hp.graticule()
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close()


def save_colored_points(theta, phi, values, title, outpath, label, cmap="viridis"):
    """Save a mollview with points colored by a value."""
    hp.mollview(np.zeros(hp.nside2npix(DEFAULT_NSIDE)), title=title)
    sc = hp.projscatter(theta, phi, s=25, c=values, cmap=cmap)
    hp.graticule()
    cbar = plt.colorbar(sc, orientation="horizontal", pad=0.05)
    cbar.set_label(label)
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close()


def save_publication_figure(gw_theta, gw_phi, grb_theta, grb_phi, gw_count, grb_count, outpath):
    """Save a combined GW+GRB points figure."""
    fig = plt.figure(figsize=(8, 5))
    hp.mollview(
        np.zeros(hp.nside2npix(DEFAULT_NSIDE)),
        title="GW + GRB Trigger Sky Map",
        fig=fig.number
    )
    gw_sc = hp.projscatter(gw_theta, gw_phi, s=25, c="red", label="GW")
    grb_sc = hp.projscatter(grb_theta, grb_phi, s=25, c="blue", label="GRB")
    hp.graticule()

    ax = plt.gca()
    ax.legend(handles=[gw_sc, grb_sc], loc="lower left")
    ax.text(
        0.02, 0.02,
        f"GW: {gw_count}  GRB: {grb_count}",
        transform=ax.transAxes,
        fontsize=9,
        bbox=dict(facecolor="white", alpha=0.75, edgecolor="none")
    )

    plt.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    FIG_DIR.mkdir(exist_ok=True)

    gw_df, gw_theta, gw_phi = load_triggers("data/simulated/gw_triggers.csv")
    grb_df, grb_theta, grb_phi = load_triggers("data/simulated/grb_triggers.csv")

    # 1) Combined density map (GW + GRB)
    m_gw = density_map(gw_theta, gw_phi)
    m_grb = density_map(grb_theta, grb_phi)
    m_total = m_gw + m_grb
    save_mollview(m_total, "GW + GRB Triggers (density)", FIG_DIR / "gw_grb_density.png")

    # 1a) Individual density maps
    save_mollview(m_gw, "GW Triggers (density)", FIG_DIR / "gw_density.png")
    save_mollview(m_grb, "GRB Triggers (density)", FIG_DIR / "grb_density.png")

    # 1b) Joint/overlap map using normalized density product (point-based)
    gw_prob = normalize_map(m_gw)
    grb_prob = normalize_map(m_grb)
    overlap = gw_prob * grb_prob
    if np.sum(overlap) > 0:
        overlap = overlap / np.sum(overlap)
    save_mollview(
        overlap,
        "GW x GRB Overlap (normalized product)",
        FIG_DIR / "gw_grb_overlap.png",
        unit="probability"
    )

    # 1c) Smoothed maps (reflect GW large maps vs GRB small maps)
    gw_smooth = smooth_map(m_gw, config.GW_SKY_SMOOTH_FWHM_DEG)
    grb_smooth = smooth_map(m_grb, config.GRB_SKY_SMOOTH_FWHM_DEG)
    save_mollview(
        gw_smooth,
        f"GW Density (smoothed, {config.GW_SKY_SMOOTH_FWHM_DEG} deg)",
        FIG_DIR / "gw_density_smoothed.png"
    )
    save_mollview(
        grb_smooth,
        f"GRB Density (smoothed, {config.GRB_SKY_SMOOTH_FWHM_DEG} deg)",
        FIG_DIR / "grb_density_smoothed.png"
    )

    gw_smooth_prob = normalize_map(gw_smooth)
    grb_smooth_prob = normalize_map(grb_smooth)
    overlap_smooth = gw_smooth_prob * grb_smooth_prob
    if np.sum(overlap_smooth) > 0:
        overlap_smooth = overlap_smooth / np.sum(overlap_smooth)
    save_mollview(
        overlap_smooth,
        "GW x GRB Overlap (smoothed)",
        FIG_DIR / "gw_grb_overlap_smoothed.png",
        unit="probability"
    )

    # 1d) Overlay coincidences on overlap map for plausibility check
    save_overlap_with_coincidences(
        overlap_smooth,
        gw_df,
        grb_df,
        FIG_DIR / "gw_grb_overlap_with_coincidences.png",
        "GW-GRB Overlap + Coincidences"
    )

    # 2) Points colored by SNR / fluence
    if "snr" in gw_df.columns:
        save_colored_points(
            gw_theta, gw_phi, gw_df["snr"].to_numpy(),
            "GW Triggers Colored by SNR",
            FIG_DIR / "gw_points_snr.png",
            label="SNR",
            cmap="magma"
        )

    if "fluence" in grb_df.columns:
        save_colored_points(
            grb_theta, grb_phi, grb_df["fluence"].to_numpy(),
            "GRB Triggers Colored by Fluence",
            FIG_DIR / "grb_points_fluence.png",
            label="Fluence",
            cmap="plasma"
        )

    # 3) Publication-style combined figure
    save_publication_figure(
        gw_theta, gw_phi, grb_theta, grb_phi,
        gw_count=len(gw_df), grb_count=len(grb_df),
        outpath=FIG_DIR / "gw_grb_publication.png"
    )

    logging.info("Saved figures to: %s", FIG_DIR.resolve())


if __name__ == "__main__":
    main()

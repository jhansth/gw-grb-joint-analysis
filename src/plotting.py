import numpy as np
import pandas as pd
import healpy as hp
import matplotlib.pyplot as plt
from pathlib import Path

DEFAULT_NSIDE = 64
FIG_DIR = Path("figures")


def load_triggers(path):
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
    m = np.zeros(hp.nside2npix(nside))
    pix = hp.ang2pix(nside, theta, phi)
    for p in pix:
        m[p] += 1
    return m


def normalize_map(m):
    total = np.sum(m)
    if total <= 0:
        return m
    return m / total


def save_mollview(m, title, outpath, unit="counts"):
    hp.mollview(m, title=title, unit=unit)
    hp.graticule()
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close()


def save_colored_points(theta, phi, values, title, outpath, label, cmap="viridis"):
    hp.mollview(np.zeros(hp.nside2npix(DEFAULT_NSIDE)), title=title)
    sc = hp.projscatter(theta, phi, s=25, c=values, cmap=cmap)
    hp.graticule()
    cbar = plt.colorbar(sc, orientation="horizontal", pad=0.05)
    cbar.set_label(label)
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close()


def save_publication_figure(gw_theta, gw_phi, grb_theta, grb_phi, gw_count, grb_count, outpath):
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

    # 1b) Joint/overlap map using normalized density product
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

    print("Saved figures to:", FIG_DIR.resolve())


if __name__ == "__main__":
    main()

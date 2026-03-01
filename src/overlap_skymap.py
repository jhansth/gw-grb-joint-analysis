import argparse
import logging
from pathlib import Path

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute and plot overlap of two HEALPix sky maps."
    )
    parser.add_argument("--gw-map", required=True, help="GW sky map FITS path")
    parser.add_argument("--grb-map", required=True, help="GRB sky map FITS path")
    parser.add_argument(
        "--out-fig",
        default="figures/gw_grb_overlap_fits.png",
        help="Output figure path"
    )
    parser.add_argument(
        "--out-map",
        default="data/results/gw_grb_overlap_map.fits",
        help="Output overlap map FITS path"
    )
    parser.add_argument(
        "--title",
        default="GW x GRB Overlap (FITS maps)",
        help="Figure title"
    )
    return parser.parse_args()


def normalize_map(m):
    m = np.asarray(m, dtype=float)
    m = np.clip(m, 0.0, None)
    total = np.sum(m)
    if total <= 0:
        return m
    return m / total


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()

    gw_map = hp.read_map(args.gw_map, verbose=False)
    grb_map = hp.read_map(args.grb_map, verbose=False)

    if gw_map.size != grb_map.size:
        raise ValueError(
            "GW and GRB maps have different sizes. "
            "Reproject to a common NSIDE before overlap."
        )

    gw_prob = normalize_map(gw_map)
    grb_prob = normalize_map(grb_map)
    overlap = normalize_map(gw_prob * grb_prob)

    out_fig = Path(args.out_fig)
    out_fig.parent.mkdir(parents=True, exist_ok=True)

    out_map = Path(args.out_map)
    out_map.parent.mkdir(parents=True, exist_ok=True)
    hp.write_map(out_map.as_posix(), overlap, overwrite=True, dtype=np.float64)

    hp.mollview(overlap, title=args.title, unit="probability")
    hp.graticule()
    plt.savefig(out_fig, dpi=200, bbox_inches="tight")
    plt.close()

    logging.info("Saved overlap map to %s", out_map)
    logging.info("Saved overlap figure to %s", out_fig)


if __name__ == "__main__":
    main()

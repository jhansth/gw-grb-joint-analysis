from pathlib import Path

import numpy as np
import pandas as pd

import config


def angular_distance(ra1, dec1, ra2, dec2):
    return np.arccos(
        np.sin(dec1)*np.sin(dec2) +
        np.cos(dec1)*np.cos(dec2)*np.cos(ra1 - ra2)
    )


def find_coincidences(gw, grb, dt, domega):
    coincidences = []

    for _, g in gw.iterrows():
        for _, r in grb.iterrows():
            if abs(g.time_gps - r.time_gps) < dt:
                ang = angular_distance(g.ra, g.dec, r.ra, r.dec)
                if ang < domega:
                    coincidences.append((g.time_gps, r.time_gps, ang))

    return coincidences


def build_coincidence_table(gw, grb, dt, domega):
    rows = []
    for g in gw.itertuples(index=False):
        for r in grb.itertuples(index=False):
            if abs(g.time_gps - r.time_gps) < dt:
                ang = angular_distance(g.ra, g.dec, r.ra, r.dec)
                if ang < domega:
                    rows.append({
                        "gw_event_id": getattr(g, "event_id", ""),
                        "grb_event_id": getattr(r, "event_id", ""),
                        "gw_time": g.time_gps,
                        "grb_time": r.time_gps,
                        "angle_rad": ang
                    })

    columns = ["gw_event_id", "grb_event_id", "gw_time", "grb_time", "angle_rad"]
    return pd.DataFrame(rows, columns=columns)





def main():
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
    print(f"Saved {len(coincidences)} coincidences to {out_path}")


if __name__ == "__main__":
    main()

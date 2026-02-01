import numpy as np


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

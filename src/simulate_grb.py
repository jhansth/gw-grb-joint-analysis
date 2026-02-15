from pathlib import Path

import numpy as np
import pandas as pd


def simulate_grb_events(n=500, t0=1.126e9):
    times = t0 + np.sort(np.random.uniform(0, 1e4, n))
    fluence = np.random.lognormal(-7, 0.5, n)
    ra = np.random.uniform(0, 2*np.pi, n)
    dec = np.random.uniform(-np.pi/2, np.pi/2, n)

    df = pd.DataFrame({
        "time_gps": times,
        "fluence": fluence,
        "ra": ra,
        "dec": dec
    })

    df.insert(0, "event_id", [f"GRB{idx + 1:03d}" for idx in range(len(df))])
    return df


def main():
    out_dir = Path("data/simulated")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "grb_triggers.csv"

    df = simulate_grb_events()
    df.to_csv(out_path, index=False)
    print(f"Saved GRB triggers to {out_path}")


if __name__ == "__main__":
    main()

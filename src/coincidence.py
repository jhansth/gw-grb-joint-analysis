import pandas as pd


def find_coincidences(dt=5):
    """Find temporal coincidences between GW and GRB"""
    gw = pd.read_csv("data/simulated_gw/trigger_times.csv")
    grb = pd.read_csv("data/simulated_grb/trigger_times.csv")
    coincidences = []

    for _, g in gw.iterrows():
        for _, r in grb.iterrows():
            if abs(g["time"] - r["time"]) <= dt:
                coincidences.append({"GW_time": g["time"], "GRB_time": r["time"],
                                     "GW_RA": g["RA"], "GW_DEC": g["DEC"],
                                     "GRB_RA": r["RA"], "GRB_DEC": r["DEC"]})

    df = pd.DataFrame(coincidences)
    df.to_csv("data/coincidences.csv", index=False)
    print(f"{len(coincidences)} coincidences found within {dt} seconds.")
    return df


if __name__ == "__main__":
    find_coincidences()

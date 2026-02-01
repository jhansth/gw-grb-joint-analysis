import pandas as pd


def find_coincidences(gw_file, grb_file, dt=5):
    """
    Identify GW-GRB coincidences within a time window dt (seconds)
    """
    gw = pd.read_csv(gw_file)
    grb = pd.read_csv(grb_file)
    coincidences = []

    for _, g in gw.iterrows():
        for _, r in grb.iterrows():
            if abs(g['time'] - r['time']) <= dt:
                coincidences.append({
                    'GW_time': g['time'],
                    'GW_RA': g['RA'],
                    'GW_DEC': g['DEC'],
                    'GRB_time': r['time'],
                    'GRB_RA': r['RA'],
                    'GRB_DEC': r['DEC']
                })
    df = pd.DataFrame(coincidences)
    df.to_csv("data/coincidences.csv", index=False)
    print(f"Found {len(df)} coincident events.")
    return df


if __name__ == "__main__":
    find_coincidences("data/simulated_gw/trigger_times.csv",
                      "data/simulated_grb/trigger_times.csv")

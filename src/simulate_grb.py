import numpy as np
import pandas as pd


def generate_grb_triggers(num_events=50, start_time=0, end_time=1e6):
    """Generate simulated GRB triggers"""
    times = np.sort(np.random.uniform(start_time, end_time, num_events))
    ra = np.random.uniform(0, 360, num_events)
    dec = np.random.uniform(-90, 90, num_events)
    df = pd.DataFrame({"time": times, "RA": ra, "DEC": dec})
    df.to_csv("data/simulated_grb/trigger_times.csv", index=False)
    print(f"{num_events} GRB events generated.")
    return df


if __name__ == "__main__":
    generate_grb_triggers()

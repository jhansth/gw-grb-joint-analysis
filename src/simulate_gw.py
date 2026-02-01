import numpy as np
import pandas as pd
import os


def generate_gw_triggers(num_events=100, start_time=0, end_time=1e6):
    """Generate simulated GW events"""
    os.makedirs("data/simulated_gw", exist_ok=True)
    times = np.sort(np.random.uniform(start_time, end_time, num_events))
    ra = np.random.uniform(0, 360, num_events)   # Right Ascension in degrees
    dec = np.random.uniform(-90, 90, num_events)  # Declination in degrees
    df = pd.DataFrame({"time": times, "RA": ra, "DEC": dec})
    df.to_csv("data/simulated_gw/trigger_times.csv", index=False)
    print(f"{num_events} GW events generated.")
    return df


if __name__ == "__main__":
    generate_gw_triggers()

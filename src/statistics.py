import pandas as pd
import numpy as np


def compute_ranking(df):
    """
    Compute a simple coincidence ranking statistic (Λ)
    Here Λ = 1 / time difference for simplicity
    """
    df['dt'] = np.abs(df['GW_time'] - df['GRB_time'])
    df['Lambda'] = 1 / (df['dt'] + 1e-3)  # avoid division by zero
    df.to_csv("data/coincidences_ranked.csv", index=False)
    return df


if __name__ == "__main__":
    df = pd.read_csv("data/coincidences.csv")
    df_ranked = compute_ranking(df)
    print(df_ranked.head())

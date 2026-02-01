import pandas as pd
import matplotlib.pyplot as plt


def plot_sky_map(df_file):
    df = pd.read_csv(df_file)
    plt.scatter(df['GW_RA'], df['GW_DEC'], c='blue', label='GW')
    plt.scatter(df['GRB_RA'], df['GRB_DEC'], c='red', label='GRB')
    plt.xlabel("RA (deg)")
    plt.ylabel("DEC (deg)")
    plt.title("GW-GRB Coincidence Sky Map")
    plt.legend()
    plt.savefig("figures/sky_map.png")
    plt.show()


if __name__ == "__main__":
    plot_sky_map("data/coincidences_ranked.csv")

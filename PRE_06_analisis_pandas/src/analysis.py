from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


FOLDER = Path(__file__).resolve().parents[1]
DRIVERS_FILE = FOLDER / "data" / "drivers.csv"
TIMESHEET_FILE = FOLDER / "data" / "timesheet.csv"
SUMMARY_FILE = FOLDER / "submission" / "summary.csv"
PLOT_FILE = FOLDER / "submission" / "top10_drivers.png"


def plot_top10(summary):
    top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)
    top10 = top10.set_index("name")

    ax = top10["miles-logged"].plot.barh(color="tab:orange", alpha=0.6)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))
    ax.tick_params(axis="x", rotation=90)
    ax.spines["left"].set_color("lightgray")
    ax.spines["bottom"].set_color("gray")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(PLOT_FILE, bbox_inches="tight")
    plt.close()


def main():
    drivers = pd.read_csv(DRIVERS_FILE)
    timesheet = pd.read_csv(TIMESHEET_FILE)

    sum_timesheet = timesheet.groupby("driverId").sum()
    summary = pd.merge(sum_timesheet, drivers[["driverId", "name"]], on="driverId")

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_FILE, index=False)

    plot_top10(summary)


if __name__ == "__main__":
    main()

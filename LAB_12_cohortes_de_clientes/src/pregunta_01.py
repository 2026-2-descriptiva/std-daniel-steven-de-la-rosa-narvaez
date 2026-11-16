from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_FILE = ACTIVITY_DIRECTORY / "data" / "sales.csv.gz"
SUBMISSION_DIRECTORY = ACTIVITY_DIRECTORY / "submission"
CSV_FILE = SUBMISSION_DIRECTORY / "cohort_retention.csv"
PNG_FILE = SUBMISSION_DIRECTORY / "cohort_retention_heatmap.png"


def build_retention_table(sales):
    sales = sales.copy()
    sales["order_month"] = pd.to_datetime(sales["OrderDate"]).dt.to_period("M")
    sales["cohort"] = sales.groupby("CustomerID")["order_month"].transform("min")
    sales["period_index"] = (sales["order_month"] - sales["cohort"]).apply(
        lambda offset: offset.n
    )

    retention = (
        sales.groupby(["cohort", "period_index"], as_index=False)["CustomerID"]
        .nunique()
        .rename(columns={"CustomerID": "active_customers"})
        .sort_values(["cohort", "period_index"])
    )
    retention["cohort_size"] = retention.groupby("cohort")["active_customers"].transform(
        "first"
    )
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )
    retention["cohort_month"] = retention["cohort"].astype(str)
    return retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ].reset_index(drop=True)


def plot_retention_heatmap(retention):
    matrix = retention.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )
    colormap = plt.get_cmap("Blues").copy()
    colormap.set_bad("white")

    figure, axes = plt.subplots(figsize=(9, 6))
    image = axes.imshow(matrix.values, cmap=colormap, vmin=0, vmax=1, aspect="auto")
    for row, cohort in enumerate(matrix.index):
        for column, period in enumerate(matrix.columns):
            value = matrix.loc[cohort, period]
            if pd.notna(value):
                axes.text(
                    column,
                    row,
                    f"{value:.0%}",
                    ha="center",
                    va="center",
                    color="white" if value > 0.6 else "black",
                    fontsize=9,
                )
    axes.set_xticks(range(len(matrix.columns)), matrix.columns)
    axes.set_yticks(range(len(matrix.index)), matrix.index)
    axes.set_xlabel("Meses desde la primera compra")
    axes.set_ylabel("Cohorte (mes de la primera compra)")
    axes.set_title("Retención de clientes por cohorte")
    colorbar = figure.colorbar(image, ax=axes)
    colorbar.ax.yaxis.set_major_formatter(
        matplotlib.ticker.PercentFormatter(xmax=1)
    )
    figure.tight_layout()
    figure.savefig(PNG_FILE, dpi=150)
    plt.close(figure)


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    sales = pd.read_csv(DATA_FILE)
    retention = build_retention_table(sales)

    SUBMISSION_DIRECTORY.mkdir(exist_ok=True)
    retention.to_csv(CSV_FILE, index=False)
    plot_retention_heatmap(retention)

    return retention

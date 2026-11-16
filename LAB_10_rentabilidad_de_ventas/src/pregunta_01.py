from pathlib import Path

import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_FILE = ACTIVITY_DIRECTORY / "data" / "superstore_orders.csv.gz"
SUBMISSION_DIRECTORY = ACTIVITY_DIRECTORY / "submission"

DISCOUNT_BANDS = ["0%", "1%-5%", "6%-10%", "más de 10%"]
MINIMUM_SEGMENT_LINES = 100


def discount_band(discount):
    if discount == 0:
        return "0%"
    if discount <= 0.05:
        return "1%-5%"
    if discount <= 0.10:
        return "6%-10%"
    return "más de 10%"


def summarize(orders, by=None):
    orders = orders.assign(
        is_loss=orders["Profit"] < 0,
        loss=orders["Profit"].where(orders["Profit"] < 0, 0).abs(),
    )
    grouped = orders.groupby(by, sort=False) if by else orders.groupby(lambda _: 0)
    summary = grouped.agg(
        lines=("Profit", "size"),
        orders=("Order ID", "nunique"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        loss_lines=("is_loss", "sum"),
        lost_profit=("loss", "sum"),
    )
    summary["profit_margin"] = summary["profit"] / summary["sales"]
    summary["loss_line_rate"] = summary["loss_lines"] / summary["lines"]
    return summary.reset_index(drop=by is None)


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    orders = pd.read_csv(DATA_FILE, sep=";", decimal=",", encoding="utf-8-sig")
    orders["discount_band"] = orders["Discount"].map(discount_band)

    profitability_summary = summarize(orders)[
        [
            "lines",
            "orders",
            "sales",
            "profit",
            "profit_margin",
            "loss_lines",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    discount_summary = (
        summarize(orders, "discount_band")
        .set_index("discount_band")
        .loc[DISCOUNT_BANDS]
        .reset_index()[
            [
                "discount_band",
                "lines",
                "sales",
                "profit",
                "profit_margin",
                "loss_line_rate",
                "lost_profit",
            ]
        ]
    )

    priority_segments = (
        summarize(orders, ["Customer Segment", "Product Category"])
        .query("lines >= @MINIMUM_SEGMENT_LINES")
        .sort_values("lost_profit", ascending=False)
        .head(5)[
            [
                "Customer Segment",
                "Product Category",
                "lines",
                "sales",
                "profit",
                "profit_margin",
                "lost_profit",
            ]
        ]
    )

    SUBMISSION_DIRECTORY.mkdir(exist_ok=True)
    profitability_summary.to_csv(
        SUBMISSION_DIRECTORY / "profitability_summary.csv", index=False
    )
    discount_summary.to_csv(SUBMISSION_DIRECTORY / "discount_summary.csv", index=False)
    priority_segments.to_csv(SUBMISSION_DIRECTORY / "priority_segments.csv", index=False)

    return profitability_summary, discount_summary, priority_segments

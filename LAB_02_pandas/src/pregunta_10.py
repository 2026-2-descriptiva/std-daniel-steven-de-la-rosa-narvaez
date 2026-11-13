from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """

    tbl0 = pd.read_csv(DATA_DIRECTORY / "tbl0.tsv", sep="\t")
    return tbl0.groupby("c1")[["c2"]].agg(
        lambda values: ":".join(str(value) for value in sorted(values))
    )

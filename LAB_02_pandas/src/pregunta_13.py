from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    tbl0 = pd.read_csv(DATA_DIRECTORY / "tbl0.tsv", sep="\t")
    tbl2 = pd.read_csv(DATA_DIRECTORY / "tbl2.tsv", sep="\t")
    return tbl0.merge(tbl2, on="c0").groupby("c1")["c5b"].sum()

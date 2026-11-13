from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """

    tbl0 = pd.read_csv(DATA_DIRECTORY / "tbl0.tsv", sep="\t")
    return tbl0.groupby("c1")["c2"].sum()

from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_08():
    """
    Retorne la tabla `data/tbl0.tsv` completa con una columna adicional
    llamada `suma`, al final, cuyo valor en cada fila es `c0 + c2`.

    Ejemplo del formato de la respuesta:

            c0 c1  c2          c3  suma
        0    0  E   1  1999-02-28     1
        1    1  A   2  1999-10-28     3
        2    2  B   5  1998-05-02     7
        ...
    """

    tbl0 = pd.read_csv(DATA_DIRECTORY / "tbl0.tsv", sep="\t")
    tbl0["suma"] = tbl0["c0"] + tbl0["c2"]
    return tbl0

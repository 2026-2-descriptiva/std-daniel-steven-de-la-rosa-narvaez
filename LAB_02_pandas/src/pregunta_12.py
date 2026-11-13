from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_12():
    """
    En `data/tbl2.tsv`, cada valor de la columna `c0` aparece en varias
    filas. Construya un DataFrame con una fila por cada valor de `c0`, en
    orden ascendente, y las columnas `c0` y `c5`. En `c5`, forme un texto
    `c5a:c5b` para cada fila de ese `c0`, ordene esos textos alfabéticamente y
    únalos separados por comas.

    Ejemplo del formato de la respuesta:

            c0                             c5
        0    0  bbb:0,ddd:9,ggg:8,hhh:2,jjj:3
        1    1        aaa:3,ccc:2,ddd:0,hhh:9
        2    2        ccc:6,ddd:2,ggg:5,jjj:1
        ...
    """

    tbl2 = pd.read_csv(DATA_DIRECTORY / "tbl2.tsv", sep="\t")
    tbl2["c5"] = tbl2["c5a"] + ":" + tbl2["c5b"].astype(str)
    return (
        tbl2.groupby("c0")["c5"]
        .agg(lambda pairs: ",".join(sorted(pairs)))
        .reset_index()
    )

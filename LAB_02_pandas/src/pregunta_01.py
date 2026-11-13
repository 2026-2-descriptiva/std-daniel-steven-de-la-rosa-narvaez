from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """

    tbl0 = pd.read_csv(DATA_DIRECTORY / "tbl0.tsv", sep="\t")
    return len(tbl0)

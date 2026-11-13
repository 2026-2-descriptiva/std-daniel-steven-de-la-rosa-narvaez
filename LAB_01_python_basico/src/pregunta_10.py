import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    return [(row[0], len(row[3].split(",")), len(row[4].split(","))) for row in rows]

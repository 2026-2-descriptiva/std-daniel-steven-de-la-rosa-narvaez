import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    totals = {}
    for row in rows:
        totals[row[0]] = totals.get(row[0], 0) + int(row[1])
    return sorted(totals.items())

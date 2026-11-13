import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    counts = {}
    for row in rows:
        counts[row[0]] = counts.get(row[0], 0) + 1
    return sorted(counts.items())

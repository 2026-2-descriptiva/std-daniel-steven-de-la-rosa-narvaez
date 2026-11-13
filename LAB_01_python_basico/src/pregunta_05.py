import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    values = {}
    for row in rows:
        values.setdefault(row[0], []).append(int(row[1]))
    return [(letter, max(items), min(items)) for letter, items in sorted(values.items())]

import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    counts = {}
    for row in rows:
        month = row[2].split("-")[1]
        counts[month] = counts.get(month, 0) + 1
    return sorted(counts.items())

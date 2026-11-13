import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    letters = {}
    for row in rows:
        letters.setdefault(int(row[1]), []).append(row[0])
    return sorted(letters.items())

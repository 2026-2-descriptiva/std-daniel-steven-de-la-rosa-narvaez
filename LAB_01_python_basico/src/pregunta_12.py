import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    totals = {}
    for row in rows:
        metrics = sum(int(pair.split(":")[1]) for pair in row[4].split(","))
        totals[row[0]] = totals.get(row[0], 0) + metrics
    return dict(sorted(totals.items()))

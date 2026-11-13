import gzip
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        rows = [line.rstrip("\n").split("\t") for line in file]

    counts = {}
    for row in rows:
        for pair in row[4].split(","):
            key = pair.split(":")[0]
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))

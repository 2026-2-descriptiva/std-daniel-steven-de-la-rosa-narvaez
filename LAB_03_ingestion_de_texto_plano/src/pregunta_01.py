import re
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"
ROW_PATTERN = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    lines = DATA_FILE.read_text(encoding="utf-8").splitlines()

    records = []
    for line in lines[4:]:
        match = ROW_PATTERN.match(line)
        if match:
            records.append(list(match.groups()))
        elif line.strip() and records:
            records[-1][3] += " " + line.strip()

    clusters = pd.DataFrame(
        records,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )
    clusters["cluster"] = clusters["cluster"].astype(int)
    clusters["cantidad_de_palabras_clave"] = clusters[
        "cantidad_de_palabras_clave"
    ].astype(int)
    clusters["porcentaje_de_palabras_clave"] = (
        clusters["porcentaje_de_palabras_clave"].str.replace(",", ".").astype(float)
    )
    clusters["principales_palabras_clave"] = (
        clusters["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.strip()
        .str.rstrip(".")
    )
    return clusters

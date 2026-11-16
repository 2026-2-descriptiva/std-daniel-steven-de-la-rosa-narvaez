import json
from pathlib import Path

import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_FILE = ACTIVITY_DIRECTORY / "data" / "ventas.csv.gz"
REPORT_FILE = ACTIVITY_DIRECTORY / "submission" / "data_quality_report.json"

REQUIRED_COLUMNS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
]
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def normalize_columns(columns):
    return (
        columns.str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )


def count_invalid_units(units):
    numeric_units = pd.to_numeric(units.str.strip(), errors="coerce").dropna()
    is_positive_integer = (numeric_units > 0) & (numeric_units == numeric_units.round())
    return int((~is_positive_integer).sum())


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    sales = pd.read_csv(DATA_FILE, dtype=str, keep_default_na=False)
    sales.columns = normalize_columns(sales.columns)

    is_missing = sales.apply(lambda column: column.str.strip().isin(["", "N/A"]))
    emails = sales["contact_email"].str.strip()

    report = {
        "row_count": len(sales),
        "column_count": sales.shape[1],
        "missing_required_columns": sorted(set(REQUIRED_COLUMNS) - set(sales.columns)),
        "unexpected_columns": sorted(set(sales.columns) - set(REQUIRED_COLUMNS)),
        "duplicate_row_count": int(sales.duplicated().sum()),
        "duplicate_supplier_id_row_count": int(
            sales["supplier_id"].str.strip().duplicated(keep=False).sum()
        ),
        "missing_value_count_by_column": {
            column: int(count) for column, count in is_missing.sum().items()
        },
        "invalid_email_count": int((~emails.str.match(EMAIL_PATTERN)).sum()),
        "invalid_unit_count": count_invalid_units(sales["units"]),
        "country_values": sorted(sales["country"].unique()),
    }

    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report

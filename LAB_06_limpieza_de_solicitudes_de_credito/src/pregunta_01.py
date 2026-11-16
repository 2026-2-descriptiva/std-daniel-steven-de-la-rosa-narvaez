from pathlib import Path

import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_FILE = ACTIVITY_DIRECTORY / "data" / "solicitudes_de_credito.csv.gz"
SUBMISSION_FILE = ACTIVITY_DIRECTORY / "submission" / "solicitudes_de_credito.csv"

TEXT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


def clean_text(values):
    return (
        values.str.lower()
        .str.replace(r"[-_]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def clean_amount(values):
    return (
        values.astype(str)
        .str.replace(r"[$,\s]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
        .astype(int)
    )


def clean_date(values):
    values = values.astype(str).str.strip()
    dates = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
    dates = dates.fillna(pd.to_datetime(values, format="%Y/%m/%d", errors="coerce"))
    return dates.dt.strftime("%Y-%m-%d")


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    applications = pd.read_csv(DATA_FILE, sep=";", index_col=0)

    for column in TEXT_COLUMNS:
        applications[column] = clean_text(applications[column])
    applications["estrato"] = applications["estrato"].astype(int)
    applications["comuna_ciudadano"] = applications["comuna_ciudadano"].astype("Int64")
    applications["fecha_de_beneficio"] = clean_date(applications["fecha_de_beneficio"])
    applications["monto_del_credito"] = clean_amount(applications["monto_del_credito"])

    required_columns = applications.columns.drop("comuna_ciudadano")
    applications = applications.dropna(subset=required_columns).drop_duplicates()

    SUBMISSION_FILE.parent.mkdir(exist_ok=True)
    applications.to_csv(SUBMISSION_FILE, sep=";", index=False)

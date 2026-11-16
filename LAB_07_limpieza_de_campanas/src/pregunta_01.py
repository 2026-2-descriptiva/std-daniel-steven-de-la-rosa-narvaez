from pathlib import Path

import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = ACTIVITY_DIRECTORY / "data"
SUBMISSION_DIRECTORY = ACTIVITY_DIRECTORY / "submission"


def load_campaign_files():
    files = sorted(DATA_DIRECTORY.glob("bank-marketing-campaing-*.csv.gz"))
    return pd.concat(
        [pd.read_csv(file, index_col=0, compression="gzip") for file in files],
        ignore_index=True,
    )


def build_client(data):
    client = data[
        ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    ].copy()
    client["job"] = client["job"].str.replace(".", "", regex=False)
    client["job"] = client["job"].str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)
    return client


def build_campaign(data):
    campaign = data[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
        ]
    ].copy()
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)
    campaign["last_contact_date"] = pd.to_datetime(
        "2022-" + data["month"] + "-" + data["day"].astype(str), format="%Y-%b-%d"
    ).dt.strftime("%Y-%m-%d")
    return campaign


def build_economics(data):
    return data[["client_id", "cons_price_idx", "euribor_three_months"]].copy()


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    data = load_campaign_files()
    client = build_client(data)
    campaign = build_campaign(data)
    economics = build_economics(data)

    SUBMISSION_DIRECTORY.mkdir(exist_ok=True)
    client.to_csv(SUBMISSION_DIRECTORY / "client.csv", index=False)
    campaign.to_csv(SUBMISSION_DIRECTORY / "campaign.csv", index=False)
    economics.to_csv(SUBMISSION_DIRECTORY / "economics.csv", index=False)

    return client, campaign, economics

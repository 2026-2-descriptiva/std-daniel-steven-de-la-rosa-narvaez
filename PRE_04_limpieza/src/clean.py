import re
import unicodedata
from pathlib import Path

import pandas as pd


FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = FOLDER / "data" / "ventas.csv"
OUTPUT_FILE = FOLDER / "submission" / "ventas.csv"


SUPPLIER_NAMES = {
    "abbcolombialtda": "ABB Colombia Ltda.",
    "alpinaproductosalimenticios": "Alpina Productos Alimenticios",
    "amazonwebservicescolombia": "Amazon Web Services Colombia",
    "bancolombiasa": "Bancolombia S.A.",
    "cementosargossa": "Cementos Argos S.A.",
    "clarocolombia": "Claro Colombia",
    "coronasas": "Corona S.A.S.",
    "ecopetrolsa": "Ecopetrol S.A.",
    "googlecolombialtda": "Google Colombia Ltda.",
    "grupoexitosa": "Grupo Exito S.A.",
    "ibmcolombiasas": "IBM Colombia S.A.S.",
    "microsoftcolombiainc": "Microsoft Colombia Inc.",
    "nutresasa": "Nutresa S.A.",
    "oraclecolombialtda": "Oracle Colombia Ltda.",
    "postobonsa": "Postobón S.A.",
    "sapcolombiasas": "SAP Colombia S.A.S.",
    "schneiderelectric": "Schneider Electric",
    "siemenssas": "Siemens S.A.S.",
    "surasa": "Sura S.A.",
    "telefonicacolombia": "Telefonica Colombia",
}


def _normalize_key(value):
    normalized = unicodedata.normalize("NFKD", str(value))
    normalized = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    normalized = normalized.lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s+", "", normalized)


def _clean_supplier(value):
    key = _normalize_key(value)
    return SUPPLIER_NAMES.get(key, str(value).strip())


def main():
    data = pd.read_csv(INPUT_FILE, skipinitialspace=True)
    data.columns = data.columns.str.strip()
    data = data.rename(columns={"COUNTRY": "country"})
    data.loc[:, "country"] = data["country"].astype("string").str.strip().str.upper()
    data.loc[:, "country"] = data["country"].replace({"COLOMBIA": "COL", "CO": "COL"})
    data = data[data["country"] == "COL"].copy()
    data.loc[:, "supplier"] = data["supplier"].map(_clean_supplier)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False)

import hashlib
import hmac
from pathlib import Path

import pandas as pd


FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = FOLDER / "data" / "raw.csv"
OUTPUT_FILE = FOLDER / "submission" / "anonymized.csv"

SECRET_KEY = b"clave-secreta-del-programa"

CITY_TO_REGION = {
    "Medellín": "Andina",
    "Bello": "Andina",
    "Envigado": "Andina",
    "Itagüí": "Andina",
    "Rionegro": "Andina",
    "Bogotá": "Andina",
    "Manizales": "Andina",
    "Pereira": "Andina",
    "Bucaramanga": "Andina",
    "Barranquilla": "Caribe",
    "Cartagena": "Caribe",
    "Cali": "Pacífica",
}

OCCUPATION_TO_GROUP = {
    "Administradora": "Servicios profesionales",
    "Abogada": "Servicios profesionales",
    "Analista financiera": "Servicios profesionales",
    "Contadora": "Servicios profesionales",
    "Arquitecta": "Tecnología y diseño",
    "Diseñadora gráfica": "Tecnología y diseño",
    "Ingeniero de sistemas": "Tecnología y diseño",
    "Médico": "Salud y educación",
    "Enfermera": "Salud y educación",
    "Docente": "Salud y educación",
    "Comerciante": "Comercio y oficios",
    "Técnico electricista": "Comercio y oficios",
}


def mask_card(card_number):
    return "********" + str(card_number).zfill(12)[-4:]


def pseudonymize(document_id):
    digest = hmac.new(SECRET_KEY, str(document_id).encode("utf-8"), hashlib.sha256)
    return f"CUST-{digest.hexdigest()[:12].upper()}"


def age_group(age):
    start = age // 10 * 10
    return f"{start}-{start + 9}"


def main():
    raw = pd.read_csv(INPUT_FILE)

    anonymized = pd.DataFrame(
        {
            "loyalty_card_number": raw["loyalty_card_number"].map(mask_card),
            "annual_spend": raw["annual_spend"],
            "customer_id": raw["document_id"].map(pseudonymize),
            "age_group": raw["age"].map(age_group),
            "region": raw["city"].map(CITY_TO_REGION),
            "occupation_group": raw["occupation"].map(OCCUPATION_TO_GROUP),
        }
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    anonymized.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()

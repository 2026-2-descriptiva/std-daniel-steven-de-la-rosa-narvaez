import json
from pathlib import Path

import pandas as pd

ACTIVITY_DIRECTORY = Path(__file__).resolve().parents[1]
DATA_FILE = ACTIVITY_DIRECTORY / "data" / "insurance.csv.gz"
REPORT_FILE = ACTIVITY_DIRECTORY / "submission" / "privacy_report.json"
PUBLISHED_FILE = ACTIVITY_DIRECTORY / "submission" / "insurance_published.csv"

K = 5
ORIGINAL_QUASI_IDENTIFIERS = ["age", "sex", "bmi", "children", "region"]
SCHEMES = {
    "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
    "without_children": ["age_group", "sex", "bmi_group", "region"],
}


def generalize(insurance):
    insurance = insurance.copy()
    insurance["age_group"] = pd.cut(
        insurance["age"],
        bins=[18, 30, 40, 50, 65],
        labels=["18-29", "30-39", "40-49", "50-64"],
        right=False,
    ).astype(str)
    insurance["bmi_group"] = pd.cut(
        insurance["bmi"],
        bins=[float("-inf"), 18.5, 25, 30, float("inf")],
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
        right=False,
    ).astype(str)
    insurance["children_group"] = pd.cut(
        insurance["children"],
        bins=[-1, 0, 2, float("inf")],
        labels=["0", "1-2", "3+"],
    ).astype(str)
    return insurance


def class_sizes(insurance, quasi_identifiers):
    return insurance.groupby(quasi_identifiers)[quasi_identifiers[0]].transform("size")


def evaluate_scheme(insurance, quasi_identifiers):
    sizes = class_sizes(insurance, quasi_identifiers)
    published = insurance[sizes >= K]
    smoker_values = published.groupby(quasi_identifiers)["smoker"].nunique()
    classes_without_diversity = smoker_values[smoker_values == 1]
    records_without_diversity = (
        published.groupby(quasi_identifiers)["smoker"].transform("nunique") == 1
    )
    summary = {
        "quasi_identifiers": quasi_identifiers,
        "equivalence_classes": int(insurance.groupby(quasi_identifiers).ngroups),
        "k_before_suppression": int(sizes.min()),
        "suppressed_records": int((sizes < K).sum()),
        "published_records": len(published),
        "published_classes": int(published.groupby(quasi_identifiers).ngroups),
        "classes_without_smoker_diversity": len(classes_without_diversity),
        "records_without_smoker_diversity": int(records_without_diversity.sum()),
    }
    return summary, published


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    insurance = generalize(pd.read_csv(DATA_FILE))

    original_sizes = class_sizes(insurance, ORIGINAL_QUASI_IDENTIFIERS)

    schemes = {}
    published_by_scheme = {}
    for name, quasi_identifiers in SCHEMES.items():
        schemes[name], published_by_scheme[name] = evaluate_scheme(
            insurance, quasi_identifiers
        )

    selected_scheme = min(schemes, key=lambda name: schemes[name]["suppressed_records"])
    published = published_by_scheme[selected_scheme][
        SCHEMES[selected_scheme] + ["smoker", "charges"]
    ]

    report = {
        "original_k": int(original_sizes.min()),
        "original_unique_records": int((original_sizes == 1).sum()),
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": float(insurance["charges"].mean()),
        "mean_charges_published": float(published["charges"].mean()),
        "smoker_rate_original": float((insurance["smoker"] == "yes").mean()),
        "smoker_rate_published": float((published["smoker"] == "yes").mean()),
    }

    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    published.to_csv(PUBLISHED_FILE, index=False)
    return report

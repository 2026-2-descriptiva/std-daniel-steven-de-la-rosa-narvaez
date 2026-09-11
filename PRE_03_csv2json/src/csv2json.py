import csv
import json
from pathlib import Path


def convert_csv_2_json(csv_file):
    input_path = Path(csv_file)
    output_folder = input_path.parent.parent / "temp"
    output_folder.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8", newline="") as file:
        records = list(csv.DictReader(file))

    output_path = output_folder / f"{input_path.stem}.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

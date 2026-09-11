import re
import shutil
from collections import defaultdict
from pathlib import Path


DATA_FOLDER = Path(__file__).resolve().parents[1] / "data"


def initialize_folder(folder):
	folder_path = Path(folder)
	delete_folder(folder_path)
	folder_path.mkdir(parents=True, exist_ok=True)


def delete_folder(folder):
	folder_path = Path(folder)
	if folder_path.exists():
		shutil.rmtree(folder_path)


def generate_file_copies(copies):
	input_folder = Path("PRE_02_mapreduce/temp/input")
	initialize_folder(input_folder)

	for source_file in sorted(DATA_FOLDER.glob("file*.txt")):
		for copy_number in range(copies):
			target_file = input_folder / f"{source_file.stem}_{copy_number}.txt"
			shutil.copyfile(source_file, target_file)


def mapper(line):
	words = re.findall(r"[a-zA-Z]+", line.lower())
	return [(word, 1) for word in words]


def reducer(word, values):
	return word, sum(values)


def hadoop(input_folder, output_folder, mapper_fn, reducer_fn):
	grouped_values = defaultdict(list)

	for input_file in sorted(Path(input_folder).glob("*.txt")):
		with input_file.open("r", encoding="utf-8") as file:
			for line in file:
				for word, value in mapper_fn(line):
					grouped_values[word].append(value)

	output_path = Path(output_folder)
	initialize_folder(output_path)
	output_file = output_path / "part-00000"

	with output_file.open("w", encoding="utf-8") as file:
		for word in sorted(grouped_values):
			key, value = reducer_fn(word, grouped_values[word])
			file.write(f"{key}\t{value}\n")

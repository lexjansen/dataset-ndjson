from linkml.validator import validate
import ndjson
import json
from pathlib import Path

"""
Validates all Dataset-JSON v1.1 NDJSON examples. Because it validates 1 line at a time this runs slowly. 
"""


def validate_dataset(dataset_filename, standard) -> None:
    with open(dataset_filename, mode='r', encoding='utf-8') as f:
        invalid_lines = []
        data_row = {}
        reader = ndjson.reader(f)
        for line_num, json_line in enumerate(reader, 1):
            if line_num > 1:
                # LinkML schema expects an object and not a naked list
                data_row["rows"] = json_line
                report = validate(data_row, schema="dataset-ndjson.yaml", target_class="RowData")
            elif line_num == 1:
                report = validate(json_line, schema="dataset-ndjson.yaml", target_class="DatasetMetadata")
            else:
                raise ValueError(f"Error: unknown line number in ndjson: {line_num}")
            if report.results:
                invalid_lines.append(line_num)
                for result in report.results:
                    print(result.message)
        if not invalid_lines:
            print(f"The DSJ NDJSON {standard} file {dataset_filename} is valid!")
        else:
            print(f"The following DSJ NDJSON lines from {standard} file {dataset_filename} are invalid {invalid_lines}")


def validate_example_datasets(datasets, standard) -> None:
    for dataset in datasets:
        dataset_filename = Path.cwd() / "data" / "ndjson" /f"{standard}-ndjson" / f"{dataset}.ndjson"
        validate_dataset(dataset_filename, standard)


if __name__ == '__main__':
    datalist_file_path = Path.cwd() / "data" / "dataset-list.json"
    with open(datalist_file_path) as f:
        ds_lists = json.load(f)
    for standard, datasets in ds_lists.items():
        validate_example_datasets(datasets, standard)

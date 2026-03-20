import csv
import json
import os
import tomli
from pathlib import Path
from src.pipeline import *
from llama_cpp import Llama


def load_config():
    config = {}

    config_path = Path("config.toml")
    if config_path.exists():
        with open(config_path, "rb") as f:
            raw_config = tomli.load(f)
            config.update(raw_config)

    data_dir = None
    if "assignment_directory" in config:
        assignment_dir = Path(config["assignment_directory"])
        data_dir = assignment_dir / ".data"
        if not data_dir.exists():
            raise Exception("Assignment Directory is Invalid")

    if data_dir and data_dir.exists():
        metadata_path = data_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                config.update(metadata)

        students_path = data_dir / "students.csv"
        if students_path.exists():
            students = []
            with open(students_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                    students.append(cleaned_row)
            config["students"] = students

        spec_path = data_dir / "spec.md"
        if spec_path.exists():
            with open(spec_path, "r", encoding="utf-8") as f:
                config["spec"] = f.read()

    metric_prompt_dir = None
    if "metric_prompt_directory" in config:
        metric_prompt_dir = Path(config["metric_prompt_directory"])
    
    if metric_prompt_dir and metric_prompt_dir.exists():
        config["metrics"] = {}
        for file_path in metric_prompt_dir.iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as f:
                    config["metrics"][file_path.stem] = f.read()
    return config

def main():
    config = load_config()
    run_pipeline(config)
    

if __name__ == "__main__":
    main()

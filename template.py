import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

project_name = "src"

list_of_files = [
    ".github/workflows/.gitkeep",
    "sql/.gitkeep",
    "sql/ddl/.gitkeep",
    "sql/dml/.gitkeep",
    "sql/migrations/.gitkeep",
    f"{project_name}/__init__.py",
    "data/.gitkeep",
    f"{project_name}/database/.gitkeep",
    f"{project_name}/database/connection.py",
    f"{project_name}/database/models.py",
    f"{project_name}/database/schema_manager.py",
    "notebooks/eda.ipynb",
    f"{project_name}/etl/__init__.py",
    f"{project_name}/etl/extract.py",
    f"{project_name}/etl/transform.py",
    f"{project_name}/etl/load.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "tests/.gitkeep",
    ".env",
    "Dockerfile",
    "run.sh",
    ".pre-commit-config.yaml",
    "pyproject.toml",
]

for filepath in list_of_files:
    file_path = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for filename: {filename}")
    if (not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(filepath, "w", encoding="utf-8") as f:
            logging.info(f"Created file: {filename}")
    else:
        logging.info(f"File {filename} already exists.")

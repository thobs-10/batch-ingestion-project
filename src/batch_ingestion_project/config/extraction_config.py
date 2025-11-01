import pandas as pd
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import csv
from dataclasses import dataclass
import os


@dataclass
class FileExtractionConfig:
    """Configuration for file extraction."""

    source_path: Path
    file_type: str  # 'csv' or 'parquet'
    chunk_size: int = 1000
    validate_schema: bool = True
    archive_processed_data: bool = True
    archive_data_directory: bool = True
    parse_dates: Optional[List[str]] = None
    # encoding: str = "utf-8"

    def __post_init__(self):
        """Validate configuration parameters."""
        self.source_path = Path(self.source_path)
        if not self.source_path.exists():
            raise FileNotFoundError(f"Source path {self.source_path} does not exist.")
        if self.file_type not in ["csv", "parquet"]:
            raise ValueError("file_type must be either 'csv' or 'parquet'.")
        if self.chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer.")

        # always make sure we archive processed data
        if self.archive_processed_data and not self.archive_data_directory:
            self.archive_data_directory = True
            os.makedirs(self.source_path.parent / "archive", exist_ok=True)


@dataclass
class CSVDataExtractorConfig(FileExtractionConfig):
    """Configuration for CSV data extraction."""

    delimiter: str = ","
    header: bool = True
    encoding: str = "utf-8"
    file_patterns: Optional[List[str]] = None  # ['customers*.csv', 'sales*.csv']

    def __post_init__(self):
        """Validate configuration parameters."""
        super().__post_init__()

        if self.file_patterns is None:
            self.file_patterns = ["*.csv"]  # Default to all CSV files


@dataclass
class FileMetadata:
    """Metadata for extracted CSV files."""

    file_name: str
    file_size: int
    extracted_at: datetime
    row_count: int
    columns: List[str]
    validation_errors: Optional[List[str]] = None

    def __post_init__(self):
        """Post-initialization processing."""
        if self.validation_errors is None:
            self.validation_errors = []


@dataclass
class ParquetDataExtractorConfig(FileExtractionConfig):
    """Configuration for Parquet data extraction."""

    file_patterns: Optional[List[str]] = None  # ['customers*.parquet', 'sales*.parquet']

    def __post_init__(self):
        """Validate configuration parameters."""
        super().__post_init__()

        if self.file_patterns is None:
            self.file_patterns = ["*.parquet"]  # Default to all Parquet files

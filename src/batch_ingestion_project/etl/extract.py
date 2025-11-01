"""'Extract data from source systems(CSV) for this project to be ingested into raw
tables in PostgreSQL database."""

from ast import Yield
from typing import List, Optional
from abc import ABC, abstractmethod


class DataExtractionStrategy(ABC):
    @abstractmethod
    def extract(self):
        pass


class CSVExtractor(DataExtractionStrategy):
    def extract(self):
        """1. Read the configs from dotenv to get file path and whether it is a full extract or incremental.
        2. Verify file configuration.
        3. Use pandera to validate schemas of data.
        4. Read CSV file in chunks based on the configuration.
        5. Yield each chunk for further processing."""
        pass

import os
from typing import Optional, Dict, Any, List
from pydantic import Field, model_validator, BaseModel, ConfigDict
from dotenv import load_dotenv

load_dotenv()


class DatabaseSettings(BaseModel):
    """Database connection settings with validation"""

    # Database connection parameters
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port", ge=1, le=65535)
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")

    # Connection pool settings
    pool_size: int = Field(default=5, description="Connection pool size", ge=1, le=20)
    max_overflow: int = Field(default=10, description="Maximum overflow connections", ge=0, le=50)
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds", ge=1, le=300)
    pool_recycle: int = Field(default=3600, description="Pool recycle time in seconds", ge=300)

    # Extra settings
    echo: bool = Field(default=False, description="Echo SQL statements")

    # model_config: ConfigDict = {
    #     "env_prefix": "DB_",
    #     "env_file": ".env",
    #     "extra": "ignore",
    # }

    @model_validator(mode="after")
    def validate_required_fields(self) -> "DatabaseSettings":
        """Validate that required fields are provided."""
        if not all([self.database, self.username, self.password]):
            raise ValueError("Database name, username, and password must be provided")
        return self

    def get_database_url(self) -> str:
        """Generate PostgreSQL connection string."""
        return (
            f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    def get_engine_config(self) -> Dict[str, Any]:
        """Generate SQLAlchemy engine configuration dictionary."""
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "echo": self.echo,
        }


class ApplicationSettings(BaseModel):
    """Application settings"""

    # Application metadata
    app_name: str = Field(default="Batch Ingestion Project", description="Application name")
    environment: str = Field(default="development", description="Environment (dev, test, prod)")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")

    # ETL Configuration
    batch_size: int = Field(default=1000, description="Default batch size for processing")

    # model_config: ConfigDict = {
    #     "env_prefix": "APP_",
    #     "env_file": ".env",
    #     "extra": "ignore",
    # }

    @model_validator(mode="after")
    def validate_environment(self) -> "ApplicationSettings":
        """Validate environment setting."""
        valid_envs = ["development", "testing", "production"]
        if self.environment.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return self


class Settings:
    """Global settings manager."""

    def __init__(self):
        self.database = DatabaseSettings(
            database=os.environ["DB_DATABASE"],
            username=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
        )
        self.app = ApplicationSettings()

    def reload(self):
        """Reload settings from environment variables."""
        self.database = DatabaseSettings(
            database=os.environ["DB_DATABASE"],
            username=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
        )
        self.app = ApplicationSettings()


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

import os
from typing import Generator, Optional, Any, Dict
from sqlmodel import SQLModel, Session, create_engine, text
from contextlib import contextmanager
from loguru import logger
from sqlalchemy.engine import Engine
from src.batch_ingestion_project.config.settings import DatabaseSettings, settings


class DatabaseConnection:
    """
    Manages PostgreSQL database connections and sessions using SQLModel.
    Provides connection pooling, session management, and database operations.
    """

    def __init__(self, database_settings: Optional[DatabaseSettings] = None):
        """Initialize database connection using settings."""
        self.database_settings = database_settings or settings.database
        self.database_url = self.database_settings.get_database_url()
        self.engine_config = self.database_settings.get_engine_config()
        self._db_engine: Optional[Engine] = None

        if not self.database_url:
            raise ValueError(
                "Database parameters must be provided either directly or through settings"
            )

        logger.info("Validated database connection string")  # Don't log the actual URL for security

    @property
    def engine(self) -> Engine:
        """
        Get or create database engine with connection pooling.
        """
        if self._db_engine is None:
            logger.info("Creating database engine")
            try:
                if not self.database_url:
                    raise ValueError("Database URL must be provided")

                # Use the engine configuration from settings
                self._db_engine = create_engine(self.database_url, **self.engine_config)
                logger.info("Database engine created successfully")
            except Exception as e:
                logger.error(f"Failed to create database engine: {e}")
                raise
        return self._db_engine

    def get_session(self) -> Session:
        """
        Create a new SQLModel database session.

        Returns:
            SQLModel Session instance
        """
        return Session(self.engine)

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope around a series of operations using SQLModel Session.

        Usage:
            with db_connection.session_scope() as session:
                session.add(model_instance)
                # Session will be committed automatically
                # Session will be rolled back on exception

        Yields:
            SQLModel Session within transaction scope
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
            logger.debug("Database transaction committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Database transaction rolled back due to error: {e}")
            raise
        finally:
            session.close()

    def create_tables(
        self,
        metadata: Optional[Any] = None,
    ) -> None:
        """
        Create all tables defined in SQLModel metadata.

        Args:
            metadata: SQLModel metadata (defaults to SQLModel.metadata)
        """

        logger.info("Creating database tables")
        if not self._db_engine:
            raise ValueError("Database engine is not initialized")
        metadata_to_use = metadata or SQLModel.metadata
        try:
            metadata_to_use.create_all(self._db_engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    def drop_tables(
        self,
        metadata: Optional[Any] = None,
    ) -> None:
        """
        Drop all tables defined in SQLModel metadata.
        WARNING: This will delete all data!

        Args:
            metadata: SQLModel metadata (defaults to SQLModel.metadata)
        """
        if not self._db_engine:
            raise ValueError("Database engine is not initialized")
        metadata_to_use = metadata or SQLModel.metadata
        logger.warning("Dropping all database tables")
        try:
            metadata_to_use.drop_all(self._db_engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test database connectivity.

        Returns:
            True if connection successful, False otherwise
        """
        if not self._db_engine:
            raise ValueError("Database engine is not initialized")
        try:
            with self._db_engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    def close(self) -> None:
        """
        Close database engine and clean up connections.
        """
        if self._db_engine:
            logger.info("Closing database engine")
            self._db_engine.dispose()
            self._db_engine = None


# Global database connection instance
_db_connection: Optional[DatabaseConnection] = None


def get_database_connection(
    database_settings: Optional[DatabaseSettings] = None,
) -> DatabaseConnection:
    """
    Get or create global database connection instance.

    Args:
        database_settings: Database settings (optional, uses global settings if not provided)

    Returns:
        DatabaseConnection instance
    """
    global _db_connection

    if _db_connection is None:
        _db_connection = DatabaseConnection(database_settings=database_settings)

    return _db_connection


def get_session() -> Session:
    """
    Convenience function to get a database session.

    Returns:
        SQLModel Session instance
    """
    return get_database_connection().get_session()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Convenience function for transactional session scope.

    Usage:
        from src.batch_ingestion_project.database.connection import session_scope

        with session_scope() as session:
            session.add(model_instance)

    Yields:
        Database session within transaction scope
    """
    db_connection = get_database_connection()
    with db_connection.session_scope() as session:
        yield session


def init_database(create_tables: bool = False) -> DatabaseConnection:
    """
    Initialize database connection and optionally create tables.

    Args:
        create_tables: Whether to create tables automatically

    Returns:
        DatabaseConnection instance
    """
    db_connection = get_database_connection()

    # Test connection
    if not db_connection.test_connection():
        raise RuntimeError("Failed to connect to database")

    # Create tables if requested
    if create_tables:
        db_connection.create_tables()

    return db_connection


def close_database_connection() -> None:
    """Close the global database connection."""
    global _db_connection
    if _db_connection:
        _db_connection.close()
        _db_connection = None

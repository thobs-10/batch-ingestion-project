from sqlmodel import Session
from src.batch_ingestion_project.models.customer import Customer
from src.batch_ingestion_project.database.connection import DatabaseConnection

import pandas as pd
from typing import List


def load_customers(customer_data: pd.DataFrame) -> None:
    """
    Load a DataFrame of customer data into the database using ORM.

    Args:
        customer_data: DataFrame containing customer data to load
    """
    db_connection = DatabaseConnection()
    with db_connection.session_scope() as session:
        for _, row in customer_data.iterrows():
            customer = Customer(
                customer_id=row["customer_id"],
                name=row["name"],
                email=row["email"],
                phone_number=row.get("phone_number"),
                address=row["address"],
                signup_date=row.get("signup_date"),
                is_active=row.get("is_active", True),
            )
            session.add(customer)
        session.commit()

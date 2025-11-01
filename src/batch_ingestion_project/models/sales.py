from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from batch_ingestion_project.models.customer import Customer
from batch_ingestion_project.models.product import Product
from .base import BaseModel
from datetime import datetime


class Sale(BaseModel, table=True):
    __tablename__ = "sales"

    sale_id: str = Field(index=True, unique=True)
    customer_id: str = Field(foreign_key="customers.customer_id", index=True)
    product_id: str = Field(foreign_key="products.product_id", index=True)
    quantity: int = Field(default=1, gt=0)
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float = Field(default=0.0, ge=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    _updated_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    customer: Optional["Customer"] = Relationship(back_populates="sales")
    product: Optional["Product"] = Relationship(back_populates="sales")

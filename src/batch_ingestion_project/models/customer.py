from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .base import BaseModel
from datetime import datetime
from batch_ingestion_project.models.sales import Sale


class Customer(BaseModel, table=True):
    __tablename__ = "customers"

    customer_id: str = Field(index=True, unique=True)
    sale_id: str = Field(foreign_key="sales.sale_id", index=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, unique=True, max_length=255)
    phone_number: Optional[str] = Field(max_length=20)
    address: Optional[str] = Field(max_length=255)
    city: Optional[str] = Field(max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    _updated_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    sales: List["Sale"] = Relationship(back_populates="customer")

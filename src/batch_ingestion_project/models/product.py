from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .base import BaseModel
from datetime import datetime
from batch_ingestion_project.models.sales import Sale


class Product(BaseModel, table=True):
    __tablename__ = "products"

    product_id: str = Field(index=True, unique=True)
    sale_id: str = Field(foreign_key="sales.sale_id", index=True)
    product_name: str = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, max_length=100)
    sku_number: Optional[str] = Field(default=None, index=True, max_length=100, unique=True)
    price: float = Field(gt=0.0)
    stock_quantity: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    _updated_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    sales: List["Sale"] = Relationship(back_populates="product")

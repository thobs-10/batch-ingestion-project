from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    _created_at: datetime = Field(default_factory=datetime.utcnow)
    _updated_at: datetime = Field(default_factory=datetime.utcnow)

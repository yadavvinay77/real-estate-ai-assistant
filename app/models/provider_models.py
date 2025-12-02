# app/models/provider_models.py

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ServiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    category: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    rating: float = 4.5

    created_at: datetime = Field(default_factory=datetime.utcnow)

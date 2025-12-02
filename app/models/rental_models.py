# app/models/rental_models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class RentalSearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    location: Optional[str] = None
    bedrooms: Optional[int] = None
    property_type: Optional[str] = None
    furnished: Optional[bool] = None
    budget: Optional[int] = None
    garden: Optional[bool] = None
    parking: Optional[bool] = None

    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    matches: List["RentalMatch"] = Relationship(back_populates="search")


class RentalMatch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    search_id: int = Field(foreign_key="rentalsearch.id")

    property_id: int
    title: str
    location: str
    price_per_month: int
    bedrooms: int
    furnished: bool
    has_garden: Optional[bool] = None
    parking: Optional[bool] = None
    url: str
    score: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    search: RentalSearch = Relationship(back_populates="matches")

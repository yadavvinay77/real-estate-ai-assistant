# app/models/chat_models.py

from pydantic import BaseModel
from typing import List, Optional


class ChatClientMessage(BaseModel):
    text: str


class ChatOption(BaseModel):
    label: str
    value: str


class ChatPropertyCard(BaseModel):
    id: int
    title: str
    price_per_month: int
    location: str
    bedrooms: int
    furnished: bool
    has_garden: bool | None = None
    parking: bool | None = None
    url: str
    score: Optional[int] = None


class ChatBotResponse(BaseModel):
    text: str
    options: List[ChatOption] = []
    properties: List[ChatPropertyCard] = []
    show_input: bool = True

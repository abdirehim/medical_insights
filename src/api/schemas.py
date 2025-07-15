from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    message: str

class TopProduct(BaseModel):
    product: str
    mention_count: int

class ChannelActivityDaily(BaseModel):
    date: str
    message_count: int

class ChannelActivityWeekly(BaseModel):
    week: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    message_text: Optional[str]
    channel_sk: str
    message_date: Optional[str] 
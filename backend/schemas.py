from pydantic import BaseModel, field_validator
from datetime import date
from typing import List

class Hackathon(BaseModel):
    id: str
    title: str
    start_date: date
    end_date: date
    location: str
    url: str
    source: str
    tags: List[str] = []

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return v

    class config:
        orm_mode = True
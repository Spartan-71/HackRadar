from pydantic import BaseModel
from datetime import date



class Hackathon(BaseModel):
    id: str
    title: str
    start_data: date
    end_date: date
    location: str
    url: str
    source: str
    tags: list[str] = []

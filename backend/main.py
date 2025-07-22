from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from contextlib import asynccontextmanager

from backend.schemas import Hackathon
from backend.crud import get_upcoming
from backend.scheduler import start_scheduler
from backend.db import SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app =FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hackathons",response_model=List[Hackathon])
def list_hackathons(
    from_date: Optional[date] = Query(None, description="Filter hackathons starting from this date"),
    to_date: Optional[date] = Query(None, description="Filter hackathons ending before this date"),
    db: Session = Depends(get_db)
):
    """
    List upcoming hackathons with optional date filters.
    """
    return get_upcoming(db, from_date, to_date)
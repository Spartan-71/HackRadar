from fastapi import FastAPI, Depends, Query, HTTPException
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

app = FastAPI(
    title="HackRadar API",
    description="API for discovering upcoming hackathons.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/hackathons",
    response_model=List[Hackathon],
    summary="List upcoming hackathons",
    description="Get a list of upcoming hackathons. You can filter by start and end date, and by source."
)
def list_hackathons(
    from_date: Optional[date] = Query(
        None, 
        description="Only hackathons starting on or after this date (YYYY-MM-DD).",
        example="2024-07-01"
    ),
    to_date: Optional[date] = Query(
        None, 
        description="Only hackathons ending on or before this date (YYYY-MM-DD).",
        example="2024-08-01"
    ),
    source: Optional[List[str]] = Query(
        None,
        description="Filter by source(s), e.g. mlh, devfolio, dorahacks, unstop, devpost.",
        example=["mlh", "devfolio"]
    ),
    db: Session = Depends(get_db)
):
    """
    List upcoming hackathons with optional date and source filters.
    """
    hackathons = get_upcoming(db, from_date, to_date, source)
    if not hackathons:
        raise HTTPException(status_code=404, detail="No hackathons found for the given criteria.")
    return hackathons
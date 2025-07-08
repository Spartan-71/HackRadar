from adapters.devpost import fetch_devpost_hackathons
from backend.db import SessionLocal, Base, engine
from backend.crud import upsert_hackathon

from backend.schemas import Hackathon

Base.metadata.create_all(bind=engine)

def run():
    db = SessionLocal()
    all_hacks = fetch_devpost_hackathons()
    for h in all_hacks:
        upsert_hackathon(db, h)
    db.close()

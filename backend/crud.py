from sqlalchemy.orm import Session
from backend.models import HackathonDB
from backend.schemas import Hackathon

def upsert_hackathon(db: Session, hack: Hackathon):
    db_obj = db.query(HackathonDB).filter_by(id=hack.id).first()
    if db_obj:
        return db_obj
    db_obj = HackathonDB(
        id=hack.id,
        title=hack.title,
        start_date=hack.start_date,
        end_date=hack.end_date,
        location=hack.location,
        url=hack.url,
        source=hack.source,
        tags=",".join(hack.tags)
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_upcoming(db: Session, from_date=None, to_date=None, sources=None):
    q = db.query(HackathonDB)
    if from_date:
        q = q.filter(HackathonDB.start_date >= from_date)
    if to_date:
        q = q.filter(HackathonDB.end_date <= to_date)
    if sources:
        q = q.filter(HackathonDB.source.in_(sources))
    return q.order_by(HackathonDB.start_date).all()
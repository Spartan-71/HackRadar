from sqlalchemy import Column, String, Date, Text
from backend.db import Base


class HackathonDB(Base):
    __tablename__ = "hackathons"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String,nullable=False)
    url = Column(String, unique=True, nullable=False)
    mode = Column(String,nullable=False)
    status = Column(String,nullable=False)
    source = Column(String, nullable=False)
    tags = Column(Text, default="",nullable=True)
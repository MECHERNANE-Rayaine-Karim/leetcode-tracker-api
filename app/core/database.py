from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Table, Column, ForeignKey

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


problem_topics = Table(
    "problem_topics",
    Base.metadata,
    Column("topic_id", ForeignKey("topics.id"), primary_key=True ),
    Column("problem_id", ForeignKey("problems.id"), primary_key=True )
)
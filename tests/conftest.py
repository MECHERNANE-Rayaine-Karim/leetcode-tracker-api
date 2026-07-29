import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.test_database_url)
testing_session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = testing_session(bind = connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
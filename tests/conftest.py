import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.user import User, Role
from sqlalchemy import select

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


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client):
    client.post("/users/register",
        json={
            "username": "user",
            "email": "user@gmail.com",
            "password": "password"
        }
    )
    response = client.post("/users/login",
        json={
             "username": "user",
            "password": "password"
        }
    )
    return {"Authorization": f"Bearer {response.json()}"}


@pytest.fixture
def authenticated_admin(client, db_session):
    client.post(
        "/users/register",
        json={"username": "admin_user", "email": "admin@gmail.com", "password": "password"},
    )

    user = db_session.execute(select(User).where(User.username == "admin_user")).scalar_one()
    user.role = Role.ADMIN
    db_session.commit()

    response = client.post(
        "/users/login",
        json={"username": "admin_user", "password": "password"},
    )
    token = response.json()
    return {"Authorization": f"Bearer {token}"}
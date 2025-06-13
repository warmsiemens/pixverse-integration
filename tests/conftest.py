import os
import pytest

os.environ["API_KEY"] = "test_api_key"
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/postgres"


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.database import Base, get_db
from app.main import app
from app.core.config import settings


@pytest.fixture
def db_fixture():
    sqlalchemy_database_url = settings.DATABASE_URL
    # указал ту же самую бд, на проде разумеется нужно тестовую бд

    engine = create_engine(sqlalchemy_database_url)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        Base.metadata.create_all(bind=engine)

        db = testing_session_local()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_fixture):
    def override_get_db():
        yield db_fixture

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

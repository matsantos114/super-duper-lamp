from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


TEST_ENV_FILE = Path(__file__).resolve().parents[1] / ".env.test"

test_settings = Settings(_env_file=TEST_ENV_FILE)
test_database_url = make_url(test_settings.database_url)

if test_database_url.database != "running_app_test":
    raise RuntimeError("Tests must use the running_app_test database")

test_engine = create_engine(test_database_url)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    join_transaction_mode="create_savepoint",
)

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def db_client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import init_test_db, test_engine as engine
from app.main import app
from app.models import Todo, User
from tests.utils import authentication_token_from_email, get_superuser_token_headers
from app.api.deps import get_db as get_session

@pytest.fixture(scope="session", autouse=True)
def db()-> Generator[Session, None, None]:
    with Session(engine) as session:
        init_test_db(session)
        yield session
        statement = delete(Todo)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()
        print("Cleanup completed.")


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_session():
        return db

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c
        
@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient)-> dict[str, str]:
    return get_superuser_token_headers(client)

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session)-> dict[str, str]:
    return authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=db)
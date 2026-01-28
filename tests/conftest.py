import os 
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
import app.core.dictionary as dictionary

# Load the dictionary once for all tests
@pytest.fixture(scope="session")
def test_engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
    
    yield engine
    try:
        os.remove(path)
    except OSError:
        pass

# Override the get_db dependency to use the test database
@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Fresh schema per test for isolation
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a TestClient that uses the overridden get_db
@pytest.fixture(scope="function")
def client(db_session):
    # Override get_db to use our test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    dictionary.WORDS = ({"sun", "sand", "sea", "snow", "star"})

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
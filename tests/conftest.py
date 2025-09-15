import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db, Base
from app.core.config import settings
from main import app
from app.crud.user import create_user, create_role
from app.schemas.user import UserCreate
from app.core.security import create_access_token

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    """Create a test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(session):
    """Create a test client"""
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_role(session):
    """Create a test role"""
    role = create_role(session, "test_role")
    return role


@pytest.fixture
def test_user(session, test_role):
    """Create a test user"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        role_id=test_role.id
    )
    user = create_user(session, user_data)
    return user


@pytest.fixture
def test_admin_role(session):
    """Create an admin role"""
    role = create_role(session, "admin")
    return role


@pytest.fixture
def test_admin_user(session, test_admin_role):
    """Create a test admin user"""
    user_data = UserCreate(
        username="admin",
        email="admin@example.com",
        password="adminpassword",
        role_id=test_admin_role.id
    )
    user = create_user(session, user_data)
    return user


@pytest.fixture
def test_editor_role(session):
    """Create an editor role"""
    role = create_role(session, "editor")
    return role


@pytest.fixture
def test_editor_user(session, test_editor_role):
    """Create a test editor user"""
    user_data = UserCreate(
        username="editor",
        email="editor@example.com",
        password="editorpassword",
        role_id=test_editor_role.id
    )
    user = create_user(session, user_data)
    return user


@pytest.fixture
def test_token(test_user):
    """Create a test access token"""
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture
def test_admin_token(test_admin_user):
    """Create a test admin access token"""
    return create_access_token(data={"sub": str(test_admin_user.id)})


@pytest.fixture
def test_editor_token(test_editor_user):
    """Create a test editor access token"""
    return create_access_token(data={"sub": str(test_editor_user.id)})

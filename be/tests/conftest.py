import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.security import create_access_token
from src.db.session import Base, get_db
from src.main import app  # your FastAPI app
import uuid
from datetime import datetime, timedelta, timezone


# Import all models to ensure they're registered with SQLAlchemy metadata
from src.db.models.user import User, UserRole
from src.db.models.staff import Staff
from src.db.models.site import Site
from src.db.models.staff_site import StaffSite
from src.db.models.shift import Shift
from src.db.models.shift_assignment import ShiftAssignment
from src.db.models.certification import Certification
from src.db.models.staff_certification import StaffCertification
from src.db.models.incident import Incident
from src.db.models.staff_note import StaffNote

# -----------------------------
# Setup in-memory or test DB
# -----------------------------
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/workforce_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency to use test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# Fixtures
# -----------------------------

# @pytest.fixture(scope="module")
# def setup_db():
#     # Create all tables before tests
#     Base.metadata.create_all(bind=engine)
#     yield
#     # Drop tables after tests
#     Base.metadata.drop_all(bind=engine, checkfirst=True)

# @pytest.fixture(scope="module")
# def client():
#     # Create tables
#     Base.metadata.create_all(bind=engine)
#     with TestClient(app) as c:
#         yield c
#     Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def manager_token():
    # Create a JWT token for the test user
    return create_access_token({"sub": "aaaa1111-1111-aaaa-1111-aaaaaaaa1111"})

@pytest.fixture(scope="module")
def manager_client(manager_token):
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer {manager_token}"})
    return client

@pytest.fixture(scope="module")
def staff_token():
    # Create a JWT token for the test user
    return create_access_token({"sub": "cccc3333-3333-cccc-3333-cccccccc3333"})

@pytest.fixture(scope="module")
def staff_client(staff_token):
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer {staff_token}"})
    return client
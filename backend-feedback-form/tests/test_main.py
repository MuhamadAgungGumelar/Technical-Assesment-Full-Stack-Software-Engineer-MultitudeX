from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base, Scores, Users
from httpx import AsyncClient
from sqlalchemy import insert
import pytest
import configparser

# Read database configuration from alembic.ini
config = configparser.ConfigParser()
config.read('alembic.ini')

# Retrieve the testing database URL from the configuration
SQLALCHEMY_DATABASE_URL = config['alembic']['sqlalchemytest.url']

# Create an async engine for SQLAlchemy using the testing database URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a sessionmaker configured for async sessions with the testing engine
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Override the get_db dependency to use the async testing database session
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# Apply the dependency override in the FastAPI application
app.dependency_overrides[get_db] = override_get_db

# Fixture to setup and teardown the testing environment
@pytest.fixture(autouse=True, scope="module")
async def setup_and_teardown():
    # Establish a connection to the database
    async with engine.begin() as conn:
        # Create all tables defined in the Base's metadata
        await conn.run_sync(Base.metadata.create_all)
        
        # Insert initial data into 'scores' table for testing purposes
        await conn.execute(insert(Scores).values([
            {"id": 99, "score": 5},  # Example data
            {"id": 100, "score": 4},  # Example data
        ]))

        # Insert initial data into 'users' table for testing purposes
        await conn.execute(insert(Users).values([
            {"id": 99, "username": "test_user"},  # Example data
            {"id": 100, "username": "another_user"},  # Example data
        ]))
        
    # Yield execution to the test cases
    yield
    
    # Clean up: Drop all tables after tests are completed
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Async client fixture for testing with httpx
@pytest.fixture
async def async_client():
    # Use AsyncClient to interact with the FastAPI application running locally
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Test case to verify the creation of feedback via POST request
@pytest.mark.anyio
async def test_create_feedback(async_client):
    response = await async_client.post("/feedback/", json={"score_id": 99, 
                                                           "user_id": 99, 
                                                           "question": "What's your name?"})
    assert response.status_code == 200
    data = response.json()
    assert data["score_id"] == 99
    assert data["user_id"] == 99
    assert data["question"] == "What's your name?"

# Test case to verify the creation of username via POST request
@pytest.mark.anyio
async def test_create_username(async_client):
    response = await async_client.post("/username/", json={"username": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test"

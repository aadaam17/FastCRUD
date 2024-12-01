import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# DATABASE_URL = "postgresql+psycopg://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Base.metadata.create_all(bind=engine) # creates the model tables in postgres

# @pytest.fixture(scope="module") # scope set to module to only run fixture once at the beginning of test
# other scope parameters: function (default), session (run only once per test session)
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# client = TestClient(app)
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "tester0@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "tester1@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    
    # session.add_all([
    #     models.Post(title="first post", content="first post contents", owner_id=test_user["id"]),
    #     models.Post(title="second post", content="second post contents", owner_id=test_user["id"]),
    #     models.Post(title="third post", content="third post contents", owner_id=test_user["id"])
    #     ])
    
    post_data = [
        {
            "title": "first post",
            "content": "first post contents",
            "owner_id": test_user["id"]
        },
        {
            "title": "second post",
            "content": "second post contents",
            "owner_id": test_user["id"]
        },
        {
            "title": "third post",
            "content": "third post contents",
            "owner_id": test_user["id"]
        },
        {
            "title": "third post",
            "content": "third post contents",
            "owner_id": test_user2["id"]
        }
    ]


    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts


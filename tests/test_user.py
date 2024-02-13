import pytest
from flask import Flask
from app import create_app
from app.models.users import User
from app.db.database import db

@pytest.fixture
def app():
    app = create_app('config.TestingConfig') 
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(client):
    user_data = {
        "email": "testuser@testuser.com",
        "password": "testpassword",
        "name": "Test User",
        "mobile_number": int("123456789"),
        "country": "Test Country",
        "user_type": "customer",
        "document_number": int("123456789")
    }
    response = client.post("/register", json=user_data)

    # Assert the response status code
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    
    # Adjusted assertions to match the actual response
    response_data = response.get_json()
    assert 'id' in response_data, "Response JSON should include the user's id"
    assert response_data['message'] == "User successfully registered", "Unexpected success message in response"
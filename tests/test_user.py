import pytest
from flask import Flask
from app.models.users import User
from app.db.database import db

@pytest.fixture
def app():
    app = Flask(__name__, instance_relative_config=True)    
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_creation(client):
    # Datos del usuario de prueba
    user_data = {"username": "testuser"}
    response = client.post("/user", json=user_data)
    
    assert response.status_code == 201
    assert response.json['username'] == user_data['username']
    
    # Verificar en la base de datos
    with app.app_context():
        user = User.query.filter_by(username=user_data['username']).first()
        assert user is not None
        # Asegurar que el usuario no tiene cuentas asociadas inicialmente
        # Esto se verificaría aquí si tu modelo de User incluyera relaciones con cuentas

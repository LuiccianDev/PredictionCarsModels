import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.users_models import User
from app.api.schemas.users_schema import UserCreate
from app.api.services.user_service import create_user_service

client = TestClient(app)

# Configurar una base de datos limpia para los tests
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Crear tablas en la BD de pruebas
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Limpiar la BD después de cada test

def test_create_user(db_session: Session):
    """Prueba la creación de un usuario en la base de datos."""
    user_data = UserCreate(username="testuser", email="test@example.com", password="testpassword")
    user = create_user_service(db_session, user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_login():
    """Prueba el endpoint de login."""
    response = client.post(
        "/login", 
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_protected_route():
    """Prueba acceso a un endpoint protegido con un token válido."""
    login_response = client.post(
        "/login", 
        data={"username": "testuser", "password": "testpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 200

def test_protected_route_without_token():
    """Prueba acceso sin token (debe fallar)."""
    response = client.get("/protected-endpoint")
    assert response.status_code == 401  # No autorizado

def test_refresh_token():
    """Prueba el endpoint de refresh_token."""
    response = client.post("/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

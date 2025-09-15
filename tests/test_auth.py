import pytest
from fastapi.testclient import TestClient
from app.crud.user import create_role


class TestAuth:
    """Test authentication endpoints"""
    
    def test_login_success(self, client: TestClient, test_user, test_role):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "testpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self, client: TestClient):
        """Test login with invalid username"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client: TestClient, test_user):
        """Test login with invalid password"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_register_success(self, client: TestClient, test_role):
        """Test successful user registration"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role_id": test_role.id
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_duplicate_username(self, client: TestClient, test_user, test_role):
        """Test registration with duplicate username"""
        user_data = {
            "username": "testuser",  # Already exists
            "email": "different@example.com",
            "password": "password",
            "role_id": test_role.id
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client: TestClient, test_user, test_role):
        """Test registration with duplicate email"""
        user_data = {
            "username": "differentuser",
            "email": "test@example.com",  # Already exists
            "password": "password",
            "role_id": test_role.id
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_get_current_user(self, client: TestClient, test_token):
        """Test getting current user info"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_refresh_token(self, client: TestClient, test_token):
        """Test token refresh"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.post("/api/v1/auth/refresh", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

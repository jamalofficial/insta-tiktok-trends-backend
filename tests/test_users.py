import pytest
from fastapi.testclient import TestClient


class TestUsers:
    """Test user management endpoints"""
    
    def test_get_all_users_admin(self, client: TestClient, test_admin_token):
        """Test getting all users as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_all_users_unauthorized(self, client: TestClient, test_token):
        """Test getting all users without admin permissions"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 403
    
    def test_get_my_profile(self, client: TestClient, test_token):
        """Test getting current user's profile"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_user_by_id_admin(self, client: TestClient, test_admin_token, test_user):
        """Test getting user by ID as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.get(f"/api/v1/users/{test_user.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == "testuser"
    
    def test_get_user_by_id_unauthorized(self, client: TestClient, test_token, test_user):
        """Test getting user by ID without admin permissions"""
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get(f"/api/v1/users/{test_user.id}", headers=headers)
        assert response.status_code == 403
    
    def test_create_user_admin(self, client: TestClient, test_admin_token, test_role):
        """Test creating user as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role_id": test_role.id
        }
        response = client.post("/api/v1/users/", json=user_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
    
    def test_create_user_unauthorized(self, client: TestClient, test_token, test_role):
        """Test creating user without admin permissions"""
        headers = {"Authorization": f"Bearer {test_token}"}
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role_id": test_role.id
        }
        response = client.post("/api/v1/users/", json=user_data, headers=headers)
        assert response.status_code == 403
    
    def test_update_own_profile(self, client: TestClient, test_token, test_user):
        """Test updating own profile"""
        headers = {"Authorization": f"Bearer {test_token}"}
        update_data = {
            "username": "updateduser"
        }
        response = client.put(f"/api/v1/users/{test_user.id}", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
    
    def test_update_other_user_profile(self, client: TestClient, test_token, test_admin_user):
        """Test updating other user's profile without admin permissions"""
        headers = {"Authorization": f"Bearer {test_token}"}
        update_data = {
            "username": "hacked"
        }
        response = client.put(f"/api/v1/users/{test_admin_user.id}", json=update_data, headers=headers)
        assert response.status_code == 403
    
    def test_delete_user_admin(self, client: TestClient, test_admin_token, test_user):
        """Test deleting user as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.delete(f"/api/v1/users/{test_user.id}", headers=headers)
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_delete_own_account_admin(self, client: TestClient, test_admin_token, test_admin_user):
        """Test admin trying to delete their own account"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.delete(f"/api/v1/users/{test_admin_user.id}", headers=headers)
        assert response.status_code == 400
        assert "Cannot delete your own account" in response.json()["detail"]
    
    def test_get_roles_admin(self, client: TestClient, test_admin_token):
        """Test getting all roles as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        response = client.get("/api/v1/users/roles/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_role_admin(self, client: TestClient, test_admin_token):
        """Test creating role as admin"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        role_data = {"name": "moderator"}
        response = client.post("/api/v1/users/roles/", json=role_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "moderator"
    
    def test_create_duplicate_role(self, client: TestClient, test_admin_token):
        """Test creating duplicate role"""
        headers = {"Authorization": f"Bearer {test_admin_token}"}
        role_data = {"name": "admin"}  # Already exists
        response = client.post("/api/v1/users/roles/", json=role_data, headers=headers)
        assert response.status_code == 400
        assert "Role already exists" in response.json()["detail"]

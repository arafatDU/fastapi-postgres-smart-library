import pytest
from fastapi import status

class TestUserAPI:
    def test_create_user(self, client):
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "role": "user"
        }
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]
        assert "id" in data
    
    def test_get_user(self, client, test_user):
        user_id = test_user["id"]
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == test_user["name"]
    
    def test_get_nonexistent_user(self, client):
        # Try to get a user with ID 999 (which shouldn't exist)
        response = client.get("/api/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_user(self, client, test_user):
        user_id = test_user["id"]
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "role": "admin"
        }
        response = client.put(f"/api/users/{user_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["role"] == update_data["role"]
    
    def test_delete_user(self, client, test_user):
        user_id = test_user["id"]
        response = client.delete(f"/api/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Try to get the deleted user
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

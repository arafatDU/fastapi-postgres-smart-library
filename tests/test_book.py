import pytest
from fastapi import status

class TestBookAPI:
    def test_create_book(self, client):
        import uuid
        
        # Generate a unique ISBN
        unique_isbn = str(uuid.uuid4())[:13]
        
        book_data = {
            "title": "New Book Title",
            "author": "New Author",
            "isbn": unique_isbn,
            "copies": 10,
            "available_copies": 10
        }
        response = client.post("/api/books/", json=book_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["isbn"] == book_data["isbn"]
        assert data["copies"] == book_data["copies"]
        assert data["available_copies"] == book_data["available_copies"]
        assert "id" in data
    
    def test_get_book(self, client, test_book):
        book_id = test_book["id"]
        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == test_book["title"]
        assert data["author"] == test_book["author"]
    
    def test_get_nonexistent_book(self, client):
        # Try to get a book with ID 999 (which shouldn't exist)
        response = client.get("/api/books/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_all_books(self, client, test_book):
        response = client.get("/api/books/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_book is in the response
        book_ids = [book["id"] for book in data]
        assert test_book["id"] in book_ids
    
    def test_update_book(self, client, test_book):
        book_id = test_book["id"]
        update_data = {
            "copies": 10,
            "available_copies": 8
        }
        response = client.put(f"/api/books/{book_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == book_id
        assert data["copies"] == update_data["copies"]
        assert data["available_copies"] == update_data["available_copies"]
        assert data["isbn"] == test_book["isbn"]  # ISBN shouldn't change
    
    def test_delete_book(self, client, test_book):
        book_id = test_book["id"]
        response = client.delete(f"/api/books/{book_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Try to get the deleted book
        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_search_books(self, client, test_book):
        # Search by title
        query = test_book["title"]
        response = client.get(f"/api/books/?search={query}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_book is in the search results
        book_ids = [book["id"] for book in data]
        assert test_book["id"] in book_ids

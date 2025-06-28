import httpx
from typing import Dict, Any
from fastapi import status

from app.core.config import settings
from app.exceptions.http_exceptions import UserNotFoundException, BookNotFoundException, NoAvailableCopiesException, ServiceUnavailableException



async def get_user(user_id: int) -> Dict[str, Any]:
    url = f"{settings.user_service_url}/api/users/{user_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise UserNotFoundException()
            elif response.status_code != status.HTTP_200_OK:
                raise ServiceUnavailableException("User")
            return response.json()
    except httpx.RequestError:
        raise ServiceUnavailableException("User")



async def get_book(book_id: int) -> Dict[str, Any]:
    url = f"{settings.book_service_url}/api/books/{book_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise BookNotFoundException()
            elif response.status_code != status.HTTP_200_OK:
                raise ServiceUnavailableException("Book")
            return response.json()
    except httpx.RequestError:
        raise ServiceUnavailableException("Book")



async def update_book_availability(book_id: int, operation: str, copies: int = 1) -> Dict[str, Any]:
    url = f"{settings.book_service_url}/api/books/{book_id}/availability"
    data = {
        "available_copies": copies,
        "operation": operation
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data, timeout=5.0)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise BookNotFoundException()
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                raise NoAvailableCopiesException()
            elif response.status_code != status.HTTP_200_OK:
                raise ServiceUnavailableException("Book")
            return response.json()
    except httpx.RequestError:
        raise ServiceUnavailableException("Book")
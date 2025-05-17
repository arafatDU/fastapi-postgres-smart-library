import httpx
from typing import Dict, Any, Callable, TypeVar, Awaitable
from fastapi import status
import time
from functools import wraps

from app.core.config import settings
from app.exceptions.http_exceptions import UserNotFoundException, BookNotFoundException, NoAvailableCopiesException, ServiceUnavailableException

T = TypeVar('T')

# Circuit breaker state management
USER_SERVICE_FAILURES = 0
BOOK_SERVICE_FAILURES = 0
USER_SERVICE_LAST_FAILURE = 0
BOOK_SERVICE_LAST_FAILURE = 0
USER_SERVICE_STATE = "CLOSED"
BOOK_SERVICE_STATE = "CLOSED"

FAILURE_THRESHOLD = 5
RECOVERY_TIMEOUT = 30

def record_failure(service_name: str):
    """Record a service failure and potentially open the circuit"""
    global USER_SERVICE_FAILURES, BOOK_SERVICE_FAILURES
    global USER_SERVICE_LAST_FAILURE, BOOK_SERVICE_LAST_FAILURE
    global USER_SERVICE_STATE, BOOK_SERVICE_STATE
    
    current_time = time.time()
    
    if service_name == "User":
        USER_SERVICE_FAILURES += 1
        USER_SERVICE_LAST_FAILURE = current_time
        if USER_SERVICE_FAILURES >= FAILURE_THRESHOLD:
            USER_SERVICE_STATE = "OPEN"
    elif service_name == "Book":
        BOOK_SERVICE_FAILURES += 1
        BOOK_SERVICE_LAST_FAILURE = current_time
        if BOOK_SERVICE_FAILURES >= FAILURE_THRESHOLD:
            BOOK_SERVICE_STATE = "OPEN"

def record_success(service_name: str):
    """Record a service success and reset failure count"""
    global USER_SERVICE_FAILURES, BOOK_SERVICE_FAILURES
    global USER_SERVICE_STATE, BOOK_SERVICE_STATE
    
    if service_name == "User":
        USER_SERVICE_FAILURES = 0
        USER_SERVICE_STATE = "CLOSED"
    elif service_name == "Book":
        BOOK_SERVICE_FAILURES = 0
        BOOK_SERVICE_STATE = "CLOSED"

def is_circuit_open(service_name: str) -> bool:
    """Check if the circuit for a service is open"""
    global USER_SERVICE_STATE, BOOK_SERVICE_STATE
    global USER_SERVICE_LAST_FAILURE, BOOK_SERVICE_LAST_FAILURE
    
    current_time = time.time()
    
    if service_name == "User":
        if USER_SERVICE_STATE == "CLOSED":
            return False
        
        if USER_SERVICE_STATE == "OPEN":
            if current_time - USER_SERVICE_LAST_FAILURE > RECOVERY_TIMEOUT:
                USER_SERVICE_STATE = "HALF-OPEN"
                return False
            return True
    elif service_name == "Book":
        if BOOK_SERVICE_STATE == "CLOSED":
            return False
        
        if BOOK_SERVICE_STATE == "OPEN":
            if current_time - BOOK_SERVICE_LAST_FAILURE > RECOVERY_TIMEOUT:
                BOOK_SERVICE_STATE = "HALF-OPEN"
                return False
            return True
    
    return False

def circuit_breaker(service_name: str, excluded_exceptions=None):
    """Circuit breaker decorator for external service calls"""
    if excluded_exceptions is None:
        excluded_exceptions = []
    
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            if is_circuit_open(service_name):
                print(f"Circuit {service_name} is OPEN - failing fast")
                raise ServiceUnavailableException(service_name)
            
            try:
                result = await func(*args, **kwargs)
                if USER_SERVICE_STATE == "HALF-OPEN" or BOOK_SERVICE_STATE == "HALF-OPEN":
                    record_success(service_name)
                return result
            except tuple(excluded_exceptions) as e:
                raise e
            except Exception as e:
                record_failure(service_name)
                print(f"Circuit {service_name} failure: {str(e)}")
                raise e
        
        return wrapper
    
    return decorator

@circuit_breaker("User", excluded_exceptions=[UserNotFoundException])
async def get_user(user_id: int) -> Dict[str, Any]:
    """Get user details from the user service"""
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
    
@circuit_breaker("Book", excluded_exceptions=[BookNotFoundException])
async def get_book(book_id: int) -> Dict[str, Any]:
    """Get book details from the book service"""
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

@circuit_breaker("Book", excluded_exceptions=[BookNotFoundException, NoAvailableCopiesException])
async def update_book_availability(book_id: int, operation: str, copies: int = 1) -> Dict[str, Any]:
    """Update book availability in the book service"""
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
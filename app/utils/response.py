from fastapi import HTTPException, status
from ..exceptions import ResourceNotFoundException, BadRequestException


def not_found(detail: str = "Resource not found"):
    raise ResourceNotFoundException(detail=detail)


def bad_request(detail: str = "Bad request"):
    raise BadRequestException(detail=detail)
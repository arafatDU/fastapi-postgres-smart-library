from fastapi import HTTPException

class ResourceNotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)

class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict occurred"):
        super().__init__(status_code=409, detail=detail)
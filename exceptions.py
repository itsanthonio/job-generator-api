from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class InvalidInputException(HTTPException):
    """Raised when input validation fails"""
    def __init__(self, detail: str = "Invalid input provided"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class RateLimitException(HTTPException):
    """Raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)

class APIException(HTTPException):
    """Raised when external API fails"""
    def __init__(self, detail: str = "External API error"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)

async def security_error_handler(request: Request, exc: SecurityError):
    """Handle security errors"""
    logger.error(f"Security error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

def register_exception_handlers(app):
    """Register all exception handlers"""
    app.add_exception_handler(SecurityError, security_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)

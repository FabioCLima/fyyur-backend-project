"""
Custom exceptions for Fyyur application.
"""
from app.exceptions.base import FyyurException


class VenueNotFoundException(FyyurException):
    """Exception raised when venue is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class DuplicateVenueException(FyyurException):
    """Exception raised when trying to create duplicate venue."""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class ArtistNotFoundException(FyyurException):
    """Exception raised when artist is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class DuplicateArtistException(FyyurException):
    """Exception raised when trying to create duplicate artist."""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class ShowNotFoundException(FyyurException):
    """Exception raised when show is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ValidationException(FyyurException):
    """Exception raised for validation errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class DatabaseException(FyyurException):
    """Exception raised for database errors."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class ConflictException(FyyurException):
    """Exception raised for conflict errors (e.g., scheduling conflicts)."""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)

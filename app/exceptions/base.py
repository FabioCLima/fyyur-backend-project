"""
Base exception for Fyyur application.
"""
from typing import Optional


class FyyurException(Exception):
    """Base exception for the Fyyur application."""
    
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

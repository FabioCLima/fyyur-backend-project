"""
Base service class with common business logic.
"""
from typing import TypeVar, Generic, List, Optional, Dict, Any
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseException

T = TypeVar('T')

class BaseService(Generic[T]):
    """Base service with common business logic."""
    
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository
    
    def create(self, **kwargs) -> T:
        """Create a new record."""
        try:
            return self.repository.create(**kwargs)
        except Exception as e:
            raise DatabaseException(f"Service error creating record: {str(e)}")
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by ID."""
        try:
            return self.repository.get_by_id(id)
        except Exception as e:
            raise DatabaseException(f"Service error getting record by ID: {str(e)}")
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Get all records with optional pagination."""
        try:
            return self.repository.get_all(limit=limit, offset=offset)
        except Exception as e:
            raise DatabaseException(f"Service error getting all records: {str(e)}")
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record by ID."""
        try:
            return self.repository.update(id, **kwargs)
        except Exception as e:
            raise DatabaseException(f"Service error updating record: {str(e)}")
    
    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        try:
            return self.repository.delete(id)
        except Exception as e:
            raise DatabaseException(f"Service error deleting record: {str(e)}")
    
    def count(self) -> int:
        """Count total records."""
        try:
            return self.repository.count()
        except Exception as e:
            raise DatabaseException(f"Service error counting records: {str(e)}")
    
    def exists(self, id: int) -> bool:
        """Check if a record exists by ID."""
        try:
            return self.repository.exists(id)
        except Exception as e:
            raise DatabaseException(f"Service error checking record existence: {str(e)}")
    
    def search(self, **filters) -> List[T]:
        """Search records by filters."""
        try:
            return self.repository.search(**filters)
        except Exception as e:
            raise DatabaseException(f"Service error searching records: {str(e)}")
    
    def validate_id(self, id: int) -> None:
        """Validate that ID is positive."""
        if not isinstance(id, int) or id <= 0:
            raise DatabaseException("ID must be a positive integer")
    
    def validate_pagination(self, limit: Optional[int] = None, offset: int = 0) -> None:
        """Validate pagination parameters."""
        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            raise DatabaseException("Limit must be a positive integer")
        if not isinstance(offset, int) or offset < 0:
            raise DatabaseException("Offset must be a non-negative integer")

"""
Base repository class with common CRUD operations.
"""
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.base import BaseModel, db
from app.exceptions import DatabaseException

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model_class: type[T]):
        self.model_class = model_class
    
    def create(self, **kwargs) -> T:
        """Create a new record."""
        try:
            instance = self.model_class(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating {self.model_class.__name__}: {str(e)}")
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by ID."""
        try:
            return self.model_class.query.get(id)
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting {self.model_class.__name__} by ID: {str(e)}")
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Get all records with optional pagination."""
        try:
            query = self.model_class.query.offset(offset)
            if limit:
                query = query.limit(limit)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting all {self.model_class.__name__}: {str(e)}")
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record by ID."""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            db.session.commit()
            return instance
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error updating {self.model_class.__name__}: {str(e)}")
    
    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False
            
            db.session.delete(instance)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error deleting {self.model_class.__name__}: {str(e)}")
    
    def count(self) -> int:
        """Count total records."""
        try:
            return self.model_class.query.count()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error counting {self.model_class.__name__}: {str(e)}")
    
    def exists(self, id: int) -> bool:
        """Check if a record exists by ID."""
        try:
            return self.model_class.query.filter_by(id=id).first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error checking existence of {self.model_class.__name__}: {str(e)}")
    
    def search(self, **filters) -> List[T]:
        """Search records by filters."""
        try:
            query = self.model_class.query
            for key, value in filters.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error searching {self.model_class.__name__}: {str(e)}")

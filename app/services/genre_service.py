"""
Genre service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.models import Genre
from app.repositories import GenreRepository
from app.services.base import BaseService
from app.exceptions import DatabaseException

class GenreService(BaseService[Genre]):
    """Service for Genre business logic."""
    
    def __init__(self):
        super().__init__(GenreRepository())
    
    def get_genre_by_name(self, name: str) -> Optional[Genre]:
        """Get genre by name."""
        try:
            if not name or not name.strip():
                return None
            return self.repository.get_by_name(name.strip())
        except Exception as e:
            raise DatabaseException(f"Error getting genre by name: {str(e)}")
    
    def get_or_create_genre(self, name: str) -> Genre:
        """Get existing genre or create new one."""
        try:
            if not name or not name.strip():
                raise DatabaseException("Genre name cannot be empty")
            return self.repository.get_or_create(name.strip())
        except Exception as e:
            raise DatabaseException(f"Error getting or creating genre: {str(e)}")
    
    def get_artists_by_genre(self, genre_name: str) -> List[Any]:
        """Get artists by genre."""
        try:
            if not genre_name or not genre_name.strip():
                return []
            return self.repository.get_artists_by_genre(genre_name.strip())
        except Exception as e:
            raise DatabaseException(f"Error getting artists by genre: {str(e)}")
    
    def get_venues_by_genre(self, genre_name: str) -> List[Any]:
        """Get venues by genre."""
        try:
            if not genre_name or not genre_name.strip():
                return []
            return self.repository.get_venues_by_genre(genre_name.strip())
        except Exception as e:
            raise DatabaseException(f"Error getting venues by genre: {str(e)}")
    
    def get_popular_genres(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular genres."""
        try:
            if limit <= 0:
                raise DatabaseException("Limit must be positive")
            return self.repository.get_popular_genres(limit=limit)
        except Exception as e:
            raise DatabaseException(f"Error getting popular genres: {str(e)}")
    
    def get_genre_statistics(self) -> Dict[str, Any]:
        """Get genre statistics."""
        try:
            return self.repository.get_genre_statistics()
        except Exception as e:
            raise DatabaseException(f"Error getting genre statistics: {str(e)}")
    
    def search_genres(self, search_term: str) -> List[Genre]:
        """Search genres by name."""
        try:
            if not search_term or not search_term.strip():
                return []
            return self.repository.search_by_name(search_term.strip())
        except Exception as e:
            raise DatabaseException(f"Error searching genres: {str(e)}")
    
    def get_all_genre_names(self) -> List[str]:
        """Get all genre names."""
        try:
            return self.repository.get_all_names()
        except Exception as e:
            raise DatabaseException(f"Error getting all genre names: {str(e)}")
    
    def validate_genres(self, genre_names: List[str]) -> List[Genre]:
        """Validate genre names and return genre objects."""
        try:
            if not genre_names:
                raise DatabaseException("At least one genre is required")
            
            # Clean and validate genre names
            cleaned_names = [name.strip() for name in genre_names if name and name.strip()]
            if not cleaned_names:
                raise DatabaseException("No valid genre names provided")
            
            return self.repository.validate_genres(cleaned_names)
        except Exception as e:
            raise DatabaseException(f"Error validating genres: {str(e)}")
    
    def create_multiple_genres(self, genre_names: List[str]) -> List[Genre]:
        """Create multiple genres."""
        try:
            if not genre_names:
                raise DatabaseException("No genre names provided")
            
            # Clean genre names
            cleaned_names = [name.strip() for name in genre_names if name and name.strip()]
            if not cleaned_names:
                raise DatabaseException("No valid genre names provided")
            
            return self.repository.create_multiple(cleaned_names)
        except Exception as e:
            raise DatabaseException(f"Error creating multiple genres: {str(e)}")
    
    def get_genre_usage_stats(self) -> Dict[str, Any]:
        """Get detailed genre usage statistics."""
        try:
            stats = self.get_genre_statistics()
            popular = self.get_popular_genres(limit=5)
            
            return {
                'summary': stats,
                'top_genres': popular,
                'total_genres': len(self.get_all_genre_names())
            }
        except Exception as e:
            raise DatabaseException(f"Error getting genre usage stats: {str(e)}")
    
    def ensure_default_genres(self) -> List[Genre]:
        """Ensure default genres exist in the database."""
        try:
            from app.utils.constants import VALID_GENRES
            return self.create_multiple_genres(list(VALID_GENRES))
        except Exception as e:
            raise DatabaseException(f"Error ensuring default genres: {str(e)}")
    
    def delete_unused_genres(self) -> int:
        """Delete genres that are not used by any artist or venue."""
        try:
            # Get genres with no artists or venues
            unused_genres = Genre.query.filter(
                ~Genre.artists.any(),
                ~Genre.venues.any()
            ).all()
            
            count = len(unused_genres)
            for genre in unused_genres:
                self.repository.delete(genre.id)
            
            return count
        except Exception as e:
            raise DatabaseException(f"Error deleting unused genres: {str(e)}")

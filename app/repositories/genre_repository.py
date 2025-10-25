"""
Genre repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models import Genre, Artist, Venue, db
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseException

class GenreRepository(BaseRepository[Genre]):
    """Repository for Genre operations."""
    
    def __init__(self):
        super().__init__(Genre)
    
    def get_by_name(self, name: str) -> Optional[Genre]:
        """Get genre by name."""
        try:
            return Genre.query.filter_by(name=name).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting genre by name: {str(e)}")
    
    def get_or_create(self, name: str) -> Genre:
        """Get existing genre or create new one."""
        try:
            genre = self.get_by_name(name)
            if not genre:
                genre = Genre(name=name)
                db.session.add(genre)
                db.session.commit()
            return genre
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error getting or creating genre: {str(e)}")
    
    def get_artists_by_genre(self, genre_name: str) -> List[Artist]:
        """Get artists by genre."""
        try:
            genre = self.get_by_name(genre_name)
            if not genre:
                return []
            return genre.artists
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting artists by genre: {str(e)}")
    
    def get_venues_by_genre(self, genre_name: str) -> List[Venue]:
        """Get venues by genre."""
        try:
            genre = self.get_by_name(genre_name)
            if not genre:
                return []
            return genre.venues
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting venues by genre: {str(e)}")
    
    def get_popular_genres(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular genres by artist count."""
        try:
            genres = Genre.query.all()
            result = []
            
            for genre in genres:
                artist_count = len(genre.artists)
                venue_count = len(genre.venues)
                result.append({
                    'id': genre.id,
                    'name': genre.name,
                    'artist_count': artist_count,
                    'venue_count': venue_count,
                    'total_count': artist_count + venue_count
                })
            
            # Sort by total count and limit
            result.sort(key=lambda x: x['total_count'], reverse=True)
            return result[:limit]
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting popular genres: {str(e)}")
    
    def get_genre_statistics(self) -> Dict[str, Any]:
        """Get genre statistics."""
        try:
            total_genres = Genre.query.count()
            genres_with_artists = Genre.query.join(Genre.artists).distinct().count()
            genres_with_venues = Genre.query.join(Genre.venues).distinct().count()
            
            return {
                'total_genres': total_genres,
                'genres_with_artists': genres_with_artists,
                'genres_with_venues': genres_with_venues,
                'unused_genres': total_genres - max(genres_with_artists, genres_with_venues)
            }
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting genre statistics: {str(e)}")
    
    def search_by_name(self, name: str) -> List[Genre]:
        """Search genres by name (partial match)."""
        try:
            return Genre.query.filter(Genre.name.ilike(f'%{name}%')).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error searching genres by name: {str(e)}")
    
    def get_all_names(self) -> List[str]:
        """Get all genre names."""
        try:
            return [genre.name for genre in Genre.query.all()]
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting all genre names: {str(e)}")
    
    def validate_genres(self, genre_names: List[str]) -> List[Genre]:
        """Validate genre names and return genre objects."""
        try:
            genres = Genre.query.filter(Genre.name.in_(genre_names)).all()
            found_names = {genre.name for genre in genres}
            missing = set(genre_names) - found_names
            
            if missing:
                raise DatabaseException(f"Invalid genres: {', '.join(missing)}")
            
            return genres
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error validating genres: {str(e)}")
    
    def create_multiple(self, genre_names: List[str]) -> List[Genre]:
        """Create multiple genres."""
        try:
            genres = []
            for name in genre_names:
                existing = self.get_by_name(name)
                if not existing:
                    genre = Genre(name=name)
                    db.session.add(genre)
                    genres.append(genre)
                else:
                    genres.append(existing)
            
            db.session.commit()
            return genres
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating multiple genres: {str(e)}")

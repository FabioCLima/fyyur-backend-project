"""
Artist repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models import Artist, Genre, Show, db
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseException, DuplicateArtistException

class ArtistRepository(BaseRepository[Artist]):
    """Repository for Artist operations."""
    
    def __init__(self):
        super().__init__(Artist)
    
    def get_by_name_and_city(self, name: str, city: str) -> Optional[Artist]:
        """Get artist by name and city."""
        try:
            return Artist.query.filter_by(name=name, city=city).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting artist by name and city: {str(e)}")
    
    def get_by_city_state(self, city: str, state: str) -> List[Artist]:
        """Get artists by city and state."""
        try:
            return Artist.query.filter_by(city=city, state=state).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting artists by city and state: {str(e)}")
    
    def search_by_name(self, name: str) -> List[Artist]:
        """Search artists by name (partial match)."""
        try:
            return Artist.query.filter(Artist.name.ilike(f'%{name}%')).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error searching artists by name: {str(e)}")
    
    def get_with_shows(self, artist_id: int) -> Optional[Artist]:
        """Get artist with its shows."""
        try:
            return Artist.query.options(
                db.joinedload(Artist.shows).joinedload(Show.venue)
            ).get(artist_id)
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting artist with shows: {str(e)}")
    
    def get_upcoming_shows(self, artist_id: int) -> List[Show]:
        """Get upcoming shows for an artist."""
        try:
            from datetime import datetime
            return Show.query.filter(
                Show.artist_id == artist_id,
                Show.start_time > datetime.utcnow()
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting upcoming shows: {str(e)}")
    
    def get_past_shows(self, artist_id: int) -> List[Show]:
        """Get past shows for an artist."""
        try:
            from datetime import datetime
            return Show.query.filter(
                Show.artist_id == artist_id,
                Show.start_time < datetime.utcnow()
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting past shows: {str(e)}")
    
    def create_with_genres(self, artist_data: Dict[str, Any], genre_names: List[str]) -> Artist:
        """Create artist with genres."""
        try:
            # Check for duplicate
            existing = self.get_by_name_and_city(artist_data['name'], artist_data['city'])
            if existing:
                raise DuplicateArtistException(f"Artist '{artist_data['name']}' already exists in {artist_data['city']}")
            
            # Get genre objects
            genres = Genre.query.filter(Genre.name.in_(genre_names)).all()
            if len(genres) != len(genre_names):
                missing = set(genre_names) - {g.name for g in genres}
                raise DatabaseException(f"Invalid genres: {', '.join(missing)}")
            
            # Create artist
            artist = Artist(**artist_data)
            artist.genres = genres
            
            db.session.add(artist)
            db.session.commit()
            return artist
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating artist with genres: {str(e)}")
    
    def update_with_genres(self, artist_id: int, artist_data: Dict[str, Any], genre_names: Optional[List[str]] = None) -> Optional[Artist]:
        """Update artist with genres."""
        try:
            artist = self.get_by_id(artist_id)
            if not artist:
                return None
            
            # Check for duplicate if name or city changed
            if 'name' in artist_data or 'city' in artist_data:
                new_name = artist_data.get('name', artist.name)
                new_city = artist_data.get('city', artist.city)
                existing = self.get_by_name_and_city(new_name, new_city)
                if existing and existing.id != artist_id:
                    raise DuplicateArtistException(f"Artist '{new_name}' already exists in {new_city}")
            
            # Update artist fields
            for key, value in artist_data.items():
                if hasattr(artist, key) and key != 'genres':
                    setattr(artist, key, value)
            
            # Update genres if provided
            if genre_names is not None:
                genres = Genre.query.filter(Genre.name.in_(genre_names)).all()
                if len(genres) != len(genre_names):
                    missing = set(genre_names) - {g.name for g in genres}
                    raise DatabaseException(f"Invalid genres: {', '.join(missing)}")
                artist.genres = genres
            
            db.session.commit()
            return artist
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error updating artist with genres: {str(e)}")
    
    def get_all_with_counts(self) -> List[Dict[str, Any]]:
        """Get all artists with show counts."""
        try:
            from datetime import datetime
            artists = Artist.query.all()
            result = []
            
            for artist in artists:
                upcoming_count = Show.query.filter(
                    Show.artist_id == artist.id,
                    Show.start_time > datetime.utcnow()
                ).count()
                
                result.append({
                    'id': artist.id,
                    'name': artist.name,
                    'num_upcoming_shows': upcoming_count
                })
            
            return result
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting artists with counts: {str(e)}")

"""
Venue repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models import Venue, Genre, Show, db
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseException, DuplicateVenueException

class VenueRepository(BaseRepository[Venue]):
    """Repository for Venue operations."""
    
    def __init__(self):
        super().__init__(Venue)
    
    def get_by_name_and_city(self, name: str, city: str) -> Optional[Venue]:
        """Get venue by name and city."""
        try:
            return Venue.query.filter_by(name=name, city=city).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting venue by name and city: {str(e)}")
    
    def get_by_city_state(self, city: str, state: str) -> List[Venue]:
        """Get venues by city and state."""
        try:
            return Venue.query.filter_by(city=city, state=state).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting venues by city and state: {str(e)}")
    
    def search_by_name(self, name: str) -> List[Venue]:
        """Search venues by name (partial match)."""
        try:
            return Venue.query.filter(Venue.name.ilike(f'%{name}%')).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error searching venues by name: {str(e)}")
    
    def get_with_shows(self, venue_id: int) -> Optional[Venue]:
        """Get venue with its shows."""
        try:
            return Venue.query.options(
                db.joinedload(Venue.shows).joinedload(Show.artist)
            ).get(venue_id)
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting venue with shows: {str(e)}")
    
    def get_upcoming_shows(self, venue_id: int) -> List[Show]:
        """Get upcoming shows for a venue."""
        try:
            from datetime import datetime
            return Show.query.filter(
                Show.venue_id == venue_id,
                Show.start_time > datetime.utcnow()
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting upcoming shows: {str(e)}")
    
    def get_past_shows(self, venue_id: int) -> List[Show]:
        """Get past shows for a venue."""
        try:
            from datetime import datetime
            return Show.query.filter(
                Show.venue_id == venue_id,
                Show.start_time < datetime.utcnow()
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting past shows: {str(e)}")
    
    def create_with_genres(self, venue_data: Dict[str, Any], genre_names: List[str]) -> Venue:
        """Create venue with genres."""
        try:
            # Check for duplicate
            existing = self.get_by_name_and_city(venue_data['name'], venue_data['city'])
            if existing:
                raise DuplicateVenueException(f"Venue '{venue_data['name']}' already exists in {venue_data['city']}")
            
            # Get genre objects
            genres = Genre.query.filter(Genre.name.in_(genre_names)).all()
            if len(genres) != len(genre_names):
                missing = set(genre_names) - {g.name for g in genres}
                raise DatabaseException(f"Invalid genres: {', '.join(missing)}")
            
            # Create venue
            venue = Venue(**venue_data)
            venue.genres = genres
            
            db.session.add(venue)
            db.session.commit()
            return venue
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating venue with genres: {str(e)}")
    
    def update_with_genres(self, venue_id: int, venue_data: Dict[str, Any], genre_names: Optional[List[str]] = None) -> Optional[Venue]:
        """Update venue with genres."""
        try:
            venue = self.get_by_id(venue_id)
            if not venue:
                return None
            
            # Check for duplicate if name or city changed
            if 'name' in venue_data or 'city' in venue_data:
                new_name = venue_data.get('name', venue.name)
                new_city = venue_data.get('city', venue.city)
                existing = self.get_by_name_and_city(new_name, new_city)
                if existing and existing.id != venue_id:
                    raise DuplicateVenueException(f"Venue '{new_name}' already exists in {new_city}")
            
            # Update venue fields
            for key, value in venue_data.items():
                if hasattr(venue, key) and key != 'genres':
                    setattr(venue, key, value)
            
            # Update genres if provided
            if genre_names is not None:
                genres = Genre.query.filter(Genre.name.in_(genre_names)).all()
                if len(genres) != len(genre_names):
                    missing = set(genre_names) - {g.name for g in genres}
                    raise DatabaseException(f"Invalid genres: {', '.join(missing)}")
                venue.genres = genres
            
            db.session.commit()
            return venue
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error updating venue with genres: {str(e)}")
    
    def get_all_with_counts(self) -> List[Dict[str, Any]]:
        """Get all venues with show counts."""
        try:
            from datetime import datetime
            venues = Venue.query.all()
            result = []
            
            for venue in venues:
                upcoming_count = Show.query.filter(
                    Show.venue_id == venue.id,
                    Show.start_time > datetime.utcnow()
                ).count()
                
                result.append({
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows': upcoming_count
                })
            
            return result
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting venues with counts: {str(e)}")
    
    def get_areas(self) -> List[Dict[str, Any]]:
        """Get unique city/state combinations (areas)."""
        try:
            areas = db.session.query(Venue.city, Venue.state).distinct().all()
            result = []
            
            for city, state in areas:
                venue_count = Venue.query.filter_by(city=city, state=state).count()
                result.append({
                    'city': city,
                    'state': state,
                    'venues': venue_count
                })
            
            return result
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting areas: {str(e)}")

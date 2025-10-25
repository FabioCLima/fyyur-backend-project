"""
Show repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.models import Show, Artist, Venue, db
from app.repositories.base import BaseRepository
from app.exceptions import DatabaseException

class ShowRepository(BaseRepository[Show]):
    """Repository for Show operations."""
    
    def __init__(self):
        super().__init__(Show)
    
    def get_by_artist_and_time(self, artist_id: int, start_time) -> Optional[Show]:
        """Get show by artist and start time."""
        try:
            return Show.query.filter_by(artist_id=artist_id, start_time=start_time).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting show by artist and time: {str(e)}")
    
    def get_by_venue_and_time(self, venue_id: int, start_time) -> Optional[Show]:
        """Get show by venue and start time."""
        try:
            return Show.query.filter_by(venue_id=venue_id, start_time=start_time).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting show by venue and time: {str(e)}")
    
    def get_upcoming_shows(self, limit: Optional[int] = None) -> List[Show]:
        """Get all upcoming shows."""
        try:
            from datetime import datetime
            query = Show.query.filter(Show.start_time > datetime.utcnow())
            if limit:
                query = query.limit(limit)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting upcoming shows: {str(e)}")
    
    def get_past_shows(self, limit: Optional[int] = None) -> List[Show]:
        """Get all past shows."""
        try:
            from datetime import datetime
            query = Show.query.filter(Show.start_time < datetime.utcnow())
            if limit:
                query = query.limit(limit)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting past shows: {str(e)}")
    
    def get_shows_by_artist(self, artist_id: int) -> List[Show]:
        """Get all shows for an artist."""
        try:
            return Show.query.filter_by(artist_id=artist_id).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting shows by artist: {str(e)}")
    
    def get_shows_by_venue(self, venue_id: int) -> List[Show]:
        """Get all shows for a venue."""
        try:
            return Show.query.filter_by(venue_id=venue_id).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting shows by venue: {str(e)}")
    
    def create_with_validation(self, artist_id: int, venue_id: int, start_time) -> Show:
        """Create show with validation."""
        try:
            # Validate artist exists
            artist = Artist.query.get(artist_id)
            if not artist:
                raise DatabaseException(f"Artist with ID {artist_id} not found")
            
            # Validate venue exists
            venue = Venue.query.get(venue_id)
            if not venue:
                raise DatabaseException(f"Venue with ID {venue_id} not found")
            
            # Check for conflicts
            existing_artist_show = self.get_by_artist_and_time(artist_id, start_time)
            if existing_artist_show:
                raise DatabaseException(f"Artist {artist_id} already has a show at {start_time}")
            
            existing_venue_show = self.get_by_venue_and_time(venue_id, start_time)
            if existing_venue_show:
                raise DatabaseException(f"Venue {venue_id} already has a show at {start_time}")
            
            # Create show
            show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
            db.session.add(show)
            db.session.commit()
            return show
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(f"Error creating show: {str(e)}")
    
    def get_recent_shows(self, days: int = 30, limit: Optional[int] = None) -> List[Show]:
        """Get recent shows within specified days."""
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = Show.query.filter(Show.start_time >= cutoff_date)
            if limit:
                query = query.limit(limit)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting recent shows: {str(e)}")
    
    def get_shows_by_date_range(self, start_date, end_date) -> List[Show]:
        """Get shows within a date range."""
        try:
            return Show.query.filter(
                Show.start_time >= start_date,
                Show.start_time <= end_date
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting shows by date range: {str(e)}")
    
    def get_all_with_details(self) -> List[Dict[str, Any]]:
        """Get all shows with artist and venue details."""
        try:
            from sqlalchemy.orm import joinedload
            shows = db.session.query(Show).options(
                joinedload(Show.artist),
                joinedload(Show.venue)
            ).all()
            
            result = []
            for show in shows:
                result.append({
                    'id': show.id,
                    'artist_id': show.artist_id,
                    'artist_name': show.artist.name,
                    'artist_image_link': show.artist.image_link,
                    'venue_id': show.venue_id,
                    'venue_name': show.venue.name,
                    'venue_image_link': show.venue.image_link,
                    'start_time': show.start_time
                })
            
            return result
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting shows with details: {str(e)}")
    
    def get_show_statistics(self) -> Dict[str, int]:
        """Get show statistics."""
        try:
            from datetime import datetime
            total_shows = Show.query.count()
            upcoming_shows = Show.query.filter(Show.start_time > datetime.utcnow()).count()
            past_shows = Show.query.filter(Show.start_time < datetime.utcnow()).count()
            
            return {
                'total_shows': total_shows,
                'upcoming_shows': upcoming_shows,
                'past_shows': past_shows
            }
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error getting show statistics: {str(e)}")

"""
Show service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models import Show
from app.repositories import ShowRepository
from app.services.base import BaseService
from app.exceptions import ShowNotFoundException, DatabaseException
from app.schemas import ShowCreate, ShowResponse, ShowListItem

class ShowService(BaseService[Show]):
    """Service for Show business logic."""
    
    def __init__(self):
        super().__init__(ShowRepository())
    
    def create_show(self, show_data: ShowCreate) -> Show:
        """Create a new show with validation."""
        try:
            # Convert Pydantic model to dict
            show_dict = show_data.model_dump()
            
            # Create show with validation
            show = self.repository.create_with_validation(
                show_dict['artist_id'],
                show_dict['venue_id'],
                show_dict['start_time']
            )
            return show
        except Exception as e:
            raise DatabaseException(f"Error creating show: {str(e)}")
    
    def get_show_response(self, show_id: int) -> Optional[ShowResponse]:
        """Get show as response schema."""
        try:
            self.validate_id(show_id)
            show = self.get_by_id(show_id)
            if not show:
                raise ShowNotFoundException(f"Show with ID {show_id} not found")
            
            return ShowResponse(
                id=show.id,
                artist_id=show.artist_id,
                artist_name=show.artist.name,
                artist_image_link=show.artist.image_link,
                venue_id=show.venue_id,
                venue_name=show.venue.name,
                venue_image_link=show.venue.image_link,
                start_time=show.start_time,
                created_at=show.created_at,
                updated_at=show.updated_at
            )
        except ShowNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error getting show response: {str(e)}")
    
    def get_all_with_details(self) -> List[Dict[str, Any]]:
        """Get all shows with artist and venue details."""
        try:
            return self.repository.get_all_with_details()
        except Exception as e:
            raise DatabaseException(f"Error getting shows with details: {str(e)}")
    
    def get_upcoming_shows(self, limit: Optional[int] = None) -> List[Show]:
        """Get all upcoming shows."""
        try:
            self.validate_pagination(limit=limit)
            return self.repository.get_upcoming_shows(limit=limit)
        except Exception as e:
            raise DatabaseException(f"Error getting upcoming shows: {str(e)}")
    
    def get_past_shows(self, limit: Optional[int] = None) -> List[Show]:
        """Get all past shows."""
        try:
            self.validate_pagination(limit=limit)
            return self.repository.get_past_shows(limit=limit)
        except Exception as e:
            raise DatabaseException(f"Error getting past shows: {str(e)}")
    
    def get_shows_by_artist(self, artist_id: int) -> List[Show]:
        """Get all shows for an artist."""
        try:
            self.validate_id(artist_id)
            return self.repository.get_shows_by_artist(artist_id)
        except Exception as e:
            raise DatabaseException(f"Error getting shows by artist: {str(e)}")
    
    def get_shows_by_venue(self, venue_id: int) -> List[Show]:
        """Get all shows for a venue."""
        try:
            self.validate_id(venue_id)
            return self.repository.get_shows_by_venue(venue_id)
        except Exception as e:
            raise DatabaseException(f"Error getting shows by venue: {str(e)}")
    
    def get_recent_shows(self, days: int = 30, limit: Optional[int] = None) -> List[Show]:
        """Get recent shows within specified days."""
        try:
            if days <= 0:
                raise DatabaseException("Days must be positive")
            self.validate_pagination(limit=limit)
            return self.repository.get_recent_shows(days=days, limit=limit)
        except Exception as e:
            raise DatabaseException(f"Error getting recent shows: {str(e)}")
    
    def get_shows_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Show]:
        """Get shows within a date range."""
        try:
            if start_date >= end_date:
                raise DatabaseException("Start date must be before end date")
            return self.repository.get_shows_by_date_range(start_date, end_date)
        except Exception as e:
            raise DatabaseException(f"Error getting shows by date range: {str(e)}")
    
    def get_show_statistics(self) -> Dict[str, int]:
        """Get show statistics."""
        try:
            return self.repository.get_show_statistics()
        except Exception as e:
            raise DatabaseException(f"Error getting show statistics: {str(e)}")
    
    def get_shows_list_items(self, shows: List[Show]) -> List[ShowListItem]:
        """Convert shows to list items."""
        try:
            return [ShowListItem(
                id=show.id,
                venue_id=show.venue_id,
                venue_name=show.venue.name,
                artist_id=show.artist_id,
                artist_name=show.artist.name,
                start_time=show.start_time
            ) for show in shows]
        except Exception as e:
            raise DatabaseException(f"Error converting shows to list items: {str(e)}")
    
    def delete_show(self, show_id: int) -> bool:
        """Delete a show."""
        try:
            self.validate_id(show_id)
            
            # Check if show exists
            if not self.exists(show_id):
                raise ShowNotFoundException(f"Show with ID {show_id} not found")
            
            return self.repository.delete(show_id)
        except ShowNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error deleting show: {str(e)}")
    
    def validate_show_time(self, start_time: datetime) -> None:
        """Validate show start time."""
        if start_time <= datetime.utcnow():
            raise DatabaseException("Show start time must be in the future")
    
    def get_shows_by_genre(self, genre_name: str) -> List[Show]:
        """Get shows by genre."""
        try:
            # This would require a more complex query joining shows with artists/venues and their genres
            # For now, we'll implement a simple version
            from app.models import Artist, Venue, Genre
            
            # Get artists with this genre
            artists_with_genre = Artist.query.join(Artist.genres).filter(Genre.name == genre_name).all()
            artist_ids = [artist.id for artist in artists_with_genre]
            
            # Get venues with this genre
            venues_with_genre = Venue.query.join(Venue.genres).filter(Genre.name == genre_name).all()
            venue_ids = [venue.id for venue in venues_with_genre]
            
            # Get shows for these artists and venues
            shows = Show.query.filter(
                (Show.artist_id.in_(artist_ids)) | (Show.venue_id.in_(venue_ids))
            ).all()
            
            return shows
        except Exception as e:
            raise DatabaseException(f"Error getting shows by genre: {str(e)}")

"""
Venue service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.models import Venue, Show
from app.repositories import VenueRepository
from app.services.base import BaseService
from app.exceptions import VenueNotFoundException, DuplicateVenueException, DatabaseException
from app.schemas import VenueCreate, VenueUpdate, VenueResponse, VenueListItem

class VenueService(BaseService[Venue]):
    """Service for Venue business logic."""
    
    def __init__(self):
        super().__init__(VenueRepository())
    
    def create_venue(self, venue_data: VenueCreate) -> Venue:
        """Create a new venue with validation."""
        try:
            # Convert Pydantic model to dict
            venue_dict = venue_data.model_dump()
            genres = venue_dict.pop('genres', [])
            
            # Create venue with genres
            venue = self.repository.create_with_genres(venue_dict, genres)
            return venue
        except DuplicateVenueException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error creating venue: {str(e)}")
    
    def update_venue(self, venue_id: int, venue_data: VenueUpdate) -> Optional[Venue]:
        """Update an existing venue."""
        try:
            self.validate_id(venue_id)
            
            # Check if venue exists
            if not self.exists(venue_id):
                raise VenueNotFoundException(f"Venue with ID {venue_id} not found")
            
            # Convert Pydantic model to dict, excluding None values
            venue_dict = {k: v for k, v in venue_data.model_dump().items() if v is not None}
            genres = venue_dict.pop('genres', None)
            
            # Update venue
            venue = self.repository.update_with_genres(venue_id, venue_dict, genres)
            return venue
        except VenueNotFoundException:
            raise
        except DuplicateVenueException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error updating venue: {str(e)}")
    
    def get_venue_with_shows(self, venue_id: int) -> Optional[Venue]:
        """Get venue with its shows."""
        try:
            self.validate_id(venue_id)
            venue = self.repository.get_with_shows(venue_id)
            if not venue:
                raise VenueNotFoundException(f"Venue with ID {venue_id} not found")
            return venue
        except VenueNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error getting venue with shows: {str(e)}")
    
    def get_venue_response(self, venue_id: int) -> Optional[VenueResponse]:
        """Get venue as response schema."""
        try:
            venue = self.get_venue_with_shows(venue_id)
            if not venue:
                return None
            
            # Get shows
            upcoming_shows = self.repository.get_upcoming_shows(venue_id)
            past_shows = self.repository.get_past_shows(venue_id)
            
            # Convert to response format
            return VenueResponse(
                id=venue.id,
                name=venue.name,
                city=venue.city,
                state=venue.state,
                address=venue.address,
                phone=venue.phone,
                image_link=venue.image_link,
                facebook_link=venue.facebook_link,
                website_link=venue.website_link,
                genres=[genre.name for genre in venue.genres],
                seeking_talent=venue.seeking_talent,
                seeking_description=venue.seeking_description,
                created_at=venue.created_at,
                updated_at=venue.updated_at,
                num_upcoming_shows=len(upcoming_shows),
                num_past_shows=len(past_shows),
                upcoming_shows=[self._format_show_summary(show) for show in upcoming_shows],
                past_shows=[self._format_show_summary(show) for show in past_shows]
            )
        except Exception as e:
            raise DatabaseException(f"Error getting venue response: {str(e)}")
    
    def get_venues_by_area(self, city: str, state: str) -> List[Venue]:
        """Get venues by city and state."""
        try:
            return self.repository.get_by_city_state(city, state)
        except Exception as e:
            raise DatabaseException(f"Error getting venues by area: {str(e)}")
    
    def search_venues(self, search_term: str) -> List[Venue]:
        """Search venues by name."""
        try:
            if not search_term or not search_term.strip():
                return []
            return self.repository.search_by_name(search_term.strip())
        except Exception as e:
            raise DatabaseException(f"Error searching venues: {str(e)}")
    
    def get_venues_with_counts(self) -> List[VenueListItem]:
        """Get all venues with show counts."""
        try:
            venues_data = self.repository.get_all_with_counts()
            return [VenueListItem(**venue) for venue in venues_data]
        except Exception as e:
            raise DatabaseException(f"Error getting venues with counts: {str(e)}")
    
    def get_areas(self) -> List[Dict[str, Any]]:
        """Get unique city/state combinations."""
        try:
            return self.repository.get_areas()
        except Exception as e:
            raise DatabaseException(f"Error getting areas: {str(e)}")
    
    def delete_venue(self, venue_id: int) -> bool:
        """Delete a venue."""
        try:
            self.validate_id(venue_id)
            
            # Check if venue exists
            if not self.exists(venue_id):
                raise VenueNotFoundException(f"Venue with ID {venue_id} not found")
            
            # Check if venue has shows
            shows = self.repository.get_shows_by_venue(venue_id)
            if shows:
                raise DatabaseException(f"Cannot delete venue with {len(shows)} shows")
            
            return self.repository.delete(venue_id)
        except VenueNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error deleting venue: {str(e)}")
    
    def _format_show_summary(self, show: Show) -> Dict[str, Any]:
        """Format show for summary display."""
        return {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time
        }

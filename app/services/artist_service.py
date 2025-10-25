"""
Artist service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.models import Artist, Show
from app.repositories import ArtistRepository
from app.services.base import BaseService
from app.exceptions import ArtistNotFoundException, DuplicateArtistException, DatabaseException
from app.schemas import ArtistCreate, ArtistUpdate, ArtistResponse, ArtistListItem

class ArtistService(BaseService[Artist]):
    """Service for Artist business logic."""
    
    def __init__(self):
        super().__init__(ArtistRepository())
    
    def create_artist(self, artist_data: ArtistCreate) -> Artist:
        """Create a new artist with validation."""
        try:
            # Convert Pydantic model to dict
            artist_dict = artist_data.model_dump()
            genres = artist_dict.pop('genres', [])
            
            # Create artist with genres
            artist = self.repository.create_with_genres(artist_dict, genres)
            return artist
        except DuplicateArtistException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error creating artist: {str(e)}")
    
    def update_artist(self, artist_id: int, artist_data: ArtistUpdate) -> Optional[Artist]:
        """Update an existing artist."""
        try:
            self.validate_id(artist_id)
            
            # Check if artist exists
            if not self.exists(artist_id):
                raise ArtistNotFoundException(f"Artist with ID {artist_id} not found")
            
            # Convert Pydantic model to dict, excluding None values
            artist_dict = {k: v for k, v in artist_data.model_dump().items() if v is not None}
            genres = artist_dict.pop('genres', None)
            
            # Update artist
            artist = self.repository.update_with_genres(artist_id, artist_dict, genres)
            return artist
        except ArtistNotFoundException:
            raise
        except DuplicateArtistException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error updating artist: {str(e)}")
    
    def get_artist_with_shows(self, artist_id: int) -> Optional[Artist]:
        """Get artist with its shows."""
        try:
            self.validate_id(artist_id)
            artist = self.repository.get_with_shows(artist_id)
            if not artist:
                raise ArtistNotFoundException(f"Artist with ID {artist_id} not found")
            return artist
        except ArtistNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error getting artist with shows: {str(e)}")
    
    def get_artist_response(self, artist_id: int) -> Optional[ArtistResponse]:
        """Get artist as response schema."""
        try:
            artist = self.get_artist_with_shows(artist_id)
            if not artist:
                return None
            
            # Get shows
            upcoming_shows = self.repository.get_upcoming_shows(artist_id)
            past_shows = self.repository.get_past_shows(artist_id)
            
            # Convert to response format
            return ArtistResponse(
                id=artist.id,
                name=artist.name,
                city=artist.city,
                state=artist.state,
                phone=artist.phone,
                image_link=artist.image_link,
                facebook_link=artist.facebook_link,
                website_link=artist.website_link,
                genres=[genre.name for genre in artist.genres],
                seeking_venue=artist.seeking_venue,
                seeking_description=artist.seeking_description,
                created_at=artist.created_at,
                updated_at=artist.updated_at,
                num_upcoming_shows=len(upcoming_shows),
                num_past_shows=len(past_shows),
                upcoming_shows=[self._format_show_summary(show) for show in upcoming_shows],
                past_shows=[self._format_show_summary(show) for show in past_shows]
            )
        except Exception as e:
            raise DatabaseException(f"Error getting artist response: {str(e)}")
    
    def get_artists_by_area(self, city: str, state: str) -> List[Artist]:
        """Get artists by city and state."""
        try:
            return self.repository.get_by_city_state(city, state)
        except Exception as e:
            raise DatabaseException(f"Error getting artists by area: {str(e)}")
    
    def search_artists(self, search_term: str) -> List[Artist]:
        """Search artists by name."""
        try:
            if not search_term or not search_term.strip():
                return []
            return self.repository.search_by_name(search_term.strip())
        except Exception as e:
            raise DatabaseException(f"Error searching artists: {str(e)}")
    
    def get_artists_with_counts(self) -> List[ArtistListItem]:
        """Get all artists with show counts."""
        try:
            artists_data = self.repository.get_all_with_counts()
            return [ArtistListItem(**artist) for artist in artists_data]
        except Exception as e:
            raise DatabaseException(f"Error getting artists with counts: {str(e)}")
    
    def delete_artist(self, artist_id: int) -> bool:
        """Delete an artist."""
        try:
            self.validate_id(artist_id)
            
            # Check if artist exists
            if not self.exists(artist_id):
                raise ArtistNotFoundException(f"Artist with ID {artist_id} not found")
            
            # Check if artist has shows
            shows = self.repository.get_shows_by_artist(artist_id)
            if shows:
                raise DatabaseException(f"Cannot delete artist with {len(shows)} shows")
            
            return self.repository.delete(artist_id)
        except ArtistNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error deleting artist: {str(e)}")
    
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

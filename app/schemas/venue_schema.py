"""
Venue schemas for validation and serialization.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime

from app.schemas.common import BaseSchema, TimestampMixin


class VenueBase(BaseSchema):
    """Base venue schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=120)
    state: str = Field(..., min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    address: str = Field(..., min_length=1, max_length=120)
    
    phone: Optional[str] = Field(None, pattern=r'^\d{3}-\d{3}-\d{4}$')
    image_link: Optional[HttpUrl] = None
    facebook_link: Optional[HttpUrl] = None
    website_link: Optional[HttpUrl] = None
    
    genres: List[str] = Field(..., min_length=1)
    seeking_talent: bool = False
    seeking_description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('genres')
    @classmethod
    def validate_genres(cls, v: List[str]) -> List[str]:
        """Validate genres against allowed list."""
        valid_genres = {
            'Alternative', 'Blues', 'Classical', 'Country', 'Electronic',
            'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
            'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B',
            'Reggae', 'Rock n Roll', 'Soul', 'Other'
        }
        for genre in v:
            if genre not in valid_genres:
                raise ValueError(f'Invalid genre: {genre}')
        return v
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v: str) -> str:
        """Convert state to uppercase."""
        return v.upper()


class VenueCreate(VenueBase):
    """Schema for creating a venue."""
    pass


class VenueUpdate(BaseSchema):
    """Schema for updating a venue."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=120)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    address: Optional[str] = Field(None, min_length=1, max_length=120)
    phone: Optional[str] = Field(None, pattern=r'^\d{3}-\d{3}-\d{4}$')
    image_link: Optional[HttpUrl] = None
    facebook_link: Optional[HttpUrl] = None
    website_link: Optional[HttpUrl] = None
    genres: Optional[List[str]] = None
    seeking_talent: Optional[bool] = None
    seeking_description: Optional[str] = Field(None, max_length=500)


class ShowSummary(BaseSchema):
    """Show summary for venue/artist pages."""
    artist_id: int
    artist_name: str
    artist_image_link: Optional[str] = None
    venue_id: int
    venue_name: str
    venue_image_link: Optional[str] = None
    start_time: datetime


class VenueResponse(VenueBase, TimestampMixin):
    """Complete venue response schema."""
    id: int
    num_upcoming_shows: int = 0
    num_past_shows: int = 0
    past_shows: List[ShowSummary] = []
    upcoming_shows: List[ShowSummary] = []


class VenueListItem(BaseSchema):
    """Venue list item schema."""
    id: int
    name: str
    num_upcoming_shows: int = 0


class VenueSearchResponse(BaseSchema):
    """Venue search response schema."""
    count: int
    data: List[VenueListItem]

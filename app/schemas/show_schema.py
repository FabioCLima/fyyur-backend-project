"""
Show schemas for validation and serialization.
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from app.schemas.common import BaseSchema, TimestampMixin


class ShowBase(BaseSchema):
    """Base show schema with common fields."""
    artist_id: int = Field(..., gt=0)
    venue_id: int = Field(..., gt=0)
    start_time: datetime = Field(...)
    
    @field_validator('start_time')
    @classmethod
    def validate_future_time(cls, v: datetime) -> datetime:
        """Validate that show time is in the future."""
        if v <= datetime.utcnow():
            raise ValueError('Show time must be in the future')
        return v


class ShowCreate(ShowBase):
    """Schema for creating a show."""
    pass


class ShowResponse(ShowBase, TimestampMixin):
    """Complete show response schema."""
    id: int
    artist_name: str
    artist_image_link: str | None = None
    venue_name: str
    venue_image_link: str | None = None


class ShowListItem(BaseSchema):
    """Show list item schema."""
    id: int
    artist_name: str
    venue_name: str
    start_time: datetime

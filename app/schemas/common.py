"""
Base schemas with common functionality.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class TimestampMixin(BaseModel):
    """Mixin for timestamps."""
    created_at: datetime
    updated_at: Optional[datetime] = None

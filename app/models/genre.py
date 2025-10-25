"""
Genre model for music genres.
"""
from app.models.base import BaseModel, db


class Genre(BaseModel):
    """Genre model for music genres."""
    __tablename__ = 'genres'

    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    artists = db.relationship('Artist', secondary='artist_genres', back_populates='genres')
    venues = db.relationship('Venue', secondary='venue_genres', back_populates='genres')

    def __repr__(self) -> str:
        return f'<Genre {self.name}>'

    def to_dict(self) -> dict:
        """Convert genre to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

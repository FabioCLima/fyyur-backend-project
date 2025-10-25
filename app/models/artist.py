"""
Artist model representing musical artists.
"""
from datetime import datetime
from typing import List, Optional
from app.models.base import BaseModel, db


# Association table for artist-genre many-to-many relationship
artist_genres = db.Table(
    'artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)


class Artist(BaseModel):
    """Artist model representing musical artists."""
    __tablename__ = 'artists'

    # Basic Information
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(120))
    
    # Links
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    website_link = db.Column(db.String(200))
    
    # Seeking
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)

    # Relationships
    shows = db.relationship('Show', back_populates='artist', cascade='all, delete-orphan')
    genres = db.relationship('Genre', secondary=artist_genres, back_populates='artists')

    # Constraints
    __table_args__ = (
        db.CheckConstraint("length(state) = 2", name='ck_artist_state_length'),
        db.Index('idx_artist_city_state', 'city', 'state'),
        db.Index('idx_artist_name', 'name'),
    )

    def __repr__(self) -> str:
        return f'<Artist {self.name}>'

    @property
    def upcoming_shows(self) -> List['Show']:
        """Get upcoming shows for this artist."""
        return [show for show in self.shows if show.start_time > datetime.utcnow()]

    @property
    def past_shows(self) -> List['Show']:
        """Get past shows for this artist."""
        return [show for show in self.shows if show.start_time <= datetime.utcnow()]

    @property
    def upcoming_shows_count(self) -> int:
        """Count of upcoming shows."""
        return len(self.upcoming_shows)

    @property
    def past_shows_count(self) -> int:
        """Count of past shows."""
        return len(self.past_shows)

    def to_dict(self) -> dict:
        """Convert artist to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'genres': [genre.name for genre in self.genres],
            'upcoming_shows': [show.to_dict() for show in self.upcoming_shows],
            'past_shows': [show.to_dict() for show in self.past_shows],
            'upcoming_shows_count': self.upcoming_shows_count,
            'past_shows_count': self.past_shows_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

"""
Show model representing performances.
"""
from datetime import datetime
from app.models.base import BaseModel, db


class Show(BaseModel):
    """Show model representing performances."""
    __tablename__ = 'shows'

    # Foreign Keys
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    
    # Show Information
    start_time = db.Column(db.DateTime, nullable=False)

    # Relationships
    artist = db.relationship('Artist', back_populates='shows')
    venue = db.relationship('Venue', back_populates='shows')

    # Constraints
    __table_args__ = (
        db.UniqueConstraint('artist_id', 'start_time', name='uq_show_artist_time'),
        db.Index('idx_show_start_time', 'start_time'),
        db.Index('idx_show_venue', 'venue_id'),
        db.Index('idx_show_artist', 'artist_id'),
    )

    def __repr__(self) -> str:
        return f'<Show {self.artist.name} at {self.venue.name}>'

    def to_dict(self) -> dict:
        """Convert show to dictionary for API responses."""
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': self.start_time.isoformat(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

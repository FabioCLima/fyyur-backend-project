"""
Tests for show-related functionality.
"""
import pytest
from datetime import datetime, timedelta
from models import Show, Artist, Venue
from services.show_service import ShowService
from schemas import ShowCreate


class TestShowModel:
    """Test cases for the Show model."""
    
    def test_show_creation(self, app, sample_venue, sample_artist):
        """Test creating a show."""
        with app.app_context():
            show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            db.session.add(show)
            db.session.commit()
            
            assert show.id is not None
            assert show.artist_id == sample_artist.id
            assert show.venue_id == sample_venue.id
            assert show.artist.name == sample_artist.name
            assert show.venue.name == sample_venue.name
    
    def test_show_to_dict(self, app, sample_show):
        """Test show to_dict method."""
        with app.app_context():
            show_dict = sample_show.to_dict()
            
            assert show_dict['id'] == sample_show.id
            assert show_dict['artist_id'] == sample_show.artist_id
            assert show_dict['venue_id'] == sample_show.venue_id
            assert show_dict['artist_name'] == sample_show.artist.name
            assert show_dict['venue_name'] == sample_show.venue.name
            assert 'start_time' in show_dict


class TestShowService:
    """Test cases for the ShowService."""
    
    def test_get_all_shows(self, app, sample_show):
        """Test getting all shows."""
        with app.app_context():
            shows = ShowService.get_all_shows()
            
            assert len(shows) == 1
            assert shows[0]['id'] == sample_show.id
            assert shows[0]['artist_id'] == sample_show.artist_id
            assert shows[0]['venue_id'] == sample_show.venue_id
    
    def test_create_show(self, app, sample_venue, sample_artist):
        """Test creating a show through service."""
        with app.app_context():
            show_data = ShowCreate(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            
            show = ShowService.create_show(show_data)
            
            assert show.id is not None
            assert show.artist_id == sample_artist.id
            assert show.venue_id == sample_venue.id
    
    def test_create_show_invalid_artist(self, app, sample_venue):
        """Test creating a show with invalid artist ID."""
        with app.app_context():
            show_data = ShowCreate(
                artist_id=999,  # Non-existent artist
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            
            with pytest.raises(ValueError, match="Artist with ID 999 not found"):
                ShowService.create_show(show_data)
    
    def test_create_show_invalid_venue(self, app, sample_artist):
        """Test creating a show with invalid venue ID."""
        with app.app_context():
            show_data = ShowCreate(
                artist_id=sample_artist.id,
                venue_id=999,  # Non-existent venue
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            
            with pytest.raises(ValueError, match="Venue with ID 999 not found"):
                ShowService.create_show(show_data)
    
    def test_get_shows_by_venue(self, app, sample_venue, sample_artist):
        """Test getting shows by venue."""
        with app.app_context():
            # Create additional shows
            show1 = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            show2 = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=2)
            )
            db.session.add_all([show1, show2])
            db.session.commit()
            
            shows = ShowService.get_shows_by_venue(sample_venue.id)
            
            assert len(shows) == 2
            assert all(show.venue_id == sample_venue.id for show in shows)
    
    def test_get_shows_by_artist(self, app, sample_venue, sample_artist):
        """Test getting shows by artist."""
        with app.app_context():
            # Create additional shows
            show1 = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            show2 = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=2)
            )
            db.session.add_all([show1, show2])
            db.session.commit()
            
            shows = ShowService.get_shows_by_artist(sample_artist.id)
            
            assert len(shows) == 2
            assert all(show.artist_id == sample_artist.id for show in shows)

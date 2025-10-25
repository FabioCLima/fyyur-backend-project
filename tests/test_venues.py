"""
Tests for venue-related functionality.
"""
import pytest
from datetime import datetime, timedelta
from models import Venue, Genre, Show, Artist
from services.venue_service import VenueService
from schemas import VenueCreate, VenueUpdate


class TestVenueModel:
    """Test cases for the Venue model."""
    
    def test_venue_creation(self, app, sample_genre):
        """Test creating a venue."""
        with app.app_context():
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890'
            )
            venue.genres.append(sample_genre)
            db.session.add(venue)
            db.session.commit()
            
            assert venue.id is not None
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
            assert venue.state == 'TC'
            assert len(venue.genres) == 1
            assert venue.genres[0].name == 'Rock'
    
    def test_venue_upcoming_shows(self, app, sample_venue, sample_artist):
        """Test venue upcoming shows property."""
        with app.app_context():
            # Create a future show
            future_show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            db.session.add(future_show)
            db.session.commit()
            
            assert len(sample_venue.upcoming_shows) == 1
            assert sample_venue.upcoming_shows_count == 1
    
    def test_venue_past_shows(self, app, sample_venue, sample_artist):
        """Test venue past shows property."""
        with app.app_context():
            # Create a past show
            past_show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(past_show)
            db.session.commit()
            
            assert len(sample_venue.past_shows) == 1
            assert sample_venue.past_shows_count == 1
    
    def test_venue_to_dict(self, app, sample_venue):
        """Test venue to_dict method."""
        with app.app_context():
            venue_dict = sample_venue.to_dict()
            
            assert venue_dict['id'] == sample_venue.id
            assert venue_dict['name'] == sample_venue.name
            assert venue_dict['city'] == sample_venue.city
            assert venue_dict['state'] == sample_venue.state
            assert 'genres' in venue_dict
            assert 'upcoming_shows' in venue_dict
            assert 'past_shows' in venue_dict


class TestVenueService:
    """Test cases for the VenueService."""
    
    def test_get_all_venues(self, app, sample_venue):
        """Test getting all venues grouped by city/state."""
        with app.app_context():
            areas = VenueService.get_all_venues()
            
            assert len(areas) == 1
            assert areas[0]['city'] == 'Test City'
            assert areas[0]['state'] == 'TC'
            assert len(areas[0]['venues']) == 1
            assert areas[0]['venues'][0]['name'] == 'Test Venue'
    
    def test_get_venue_by_id(self, app, sample_venue):
        """Test getting venue by ID."""
        with app.app_context():
            venue = VenueService.get_venue_by_id(sample_venue.id)
            
            assert venue is not None
            assert venue.id == sample_venue.id
            assert venue.name == sample_venue.name
    
    def test_get_venue_by_id_not_found(self, app):
        """Test getting venue by non-existent ID."""
        with app.app_context():
            venue = VenueService.get_venue_by_id(999)
            
            assert venue is None
    
    def test_search_venues(self, app, sample_venue):
        """Test searching venues by name."""
        with app.app_context():
            # Test exact match
            response = VenueService.search_venues('Test Venue')
            assert response['count'] == 1
            assert response['data'][0]['name'] == 'Test Venue'
            
            # Test partial match
            response = VenueService.search_venues('Test')
            assert response['count'] == 1
            
            # Test case insensitive
            response = VenueService.search_venues('test venue')
            assert response['count'] == 1
            
            # Test no match
            response = VenueService.search_venues('NonExistent')
            assert response['count'] == 0
    
    def test_create_venue(self, app, sample_genre):
        """Test creating a venue through service."""
        with app.app_context():
            venue_data = VenueCreate(
                name='New Venue',
                city='New City',
                state='NC',
                address='456 New St',
                phone='987-654-3210',
                genres=['Rock']
            )
            
            venue = VenueService.create_venue(venue_data)
            
            assert venue.id is not None
            assert venue.name == 'New Venue'
            assert venue.city == 'New City'
            assert venue.state == 'NC'
            assert len(venue.genres) == 1
    
    def test_update_venue(self, app, sample_venue):
        """Test updating a venue through service."""
        with app.app_context():
            venue_data = VenueUpdate(
                name='Updated Venue',
                city='Updated City'
            )
            
            updated_venue = VenueService.update_venue(sample_venue.id, venue_data)
            
            assert updated_venue is not None
            assert updated_venue.name == 'Updated Venue'
            assert updated_venue.city == 'Updated City'
            assert updated_venue.state == sample_venue.state  # Unchanged
    
    def test_delete_venue(self, app, sample_venue):
        """Test deleting a venue through service."""
        with app.app_context():
            venue_id = sample_venue.id
            
            success = VenueService.delete_venue(venue_id)
            
            assert success is True
            
            # Verify venue is deleted
            venue = VenueService.get_venue_by_id(venue_id)
            assert venue is None
    
    def test_delete_venue_not_found(self, app):
        """Test deleting non-existent venue."""
        with app.app_context():
            success = VenueService.delete_venue(999)
            
            assert success is False

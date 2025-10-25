"""
Tests for artist-related functionality.
"""
import pytest
from datetime import datetime, timedelta
from models import Artist, Genre, Show, Venue
from services.artist_service import ArtistService
from schemas import ArtistCreate, ArtistUpdate


class TestArtistModel:
    """Test cases for the Artist model."""
    
    def test_artist_creation(self, app, sample_genre):
        """Test creating an artist."""
        with app.app_context():
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890'
            )
            artist.genres.append(sample_genre)
            db.session.add(artist)
            db.session.commit()
            
            assert artist.id is not None
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
            assert artist.state == 'TC'
            assert len(artist.genres) == 1
            assert artist.genres[0].name == 'Rock'
    
    def test_artist_upcoming_shows(self, app, sample_artist, sample_venue):
        """Test artist upcoming shows property."""
        with app.app_context():
            # Create a future show
            future_show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            db.session.add(future_show)
            db.session.commit()
            
            assert len(sample_artist.upcoming_shows) == 1
            assert sample_artist.upcoming_shows_count == 1
    
    def test_artist_past_shows(self, app, sample_artist, sample_venue):
        """Test artist past shows property."""
        with app.app_context():
            # Create a past show
            past_show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(past_show)
            db.session.commit()
            
            assert len(sample_artist.past_shows) == 1
            assert sample_artist.past_shows_count == 1
    
    def test_artist_to_dict(self, app, sample_artist):
        """Test artist to_dict method."""
        with app.app_context():
            artist_dict = sample_artist.to_dict()
            
            assert artist_dict['id'] == sample_artist.id
            assert artist_dict['name'] == sample_artist.name
            assert artist_dict['city'] == sample_artist.city
            assert artist_dict['state'] == sample_artist.state
            assert 'genres' in artist_dict
            assert 'upcoming_shows' in artist_dict
            assert 'past_shows' in artist_dict


class TestArtistService:
    """Test cases for the ArtistService."""
    
    def test_get_all_artists(self, app, sample_artist):
        """Test getting all artists."""
        with app.app_context():
            artists = ArtistService.get_all_artists()
            
            assert len(artists) == 1
            assert artists[0]['id'] == sample_artist.id
            assert artists[0]['name'] == sample_artist.name
    
    def test_get_artist_by_id(self, app, sample_artist):
        """Test getting artist by ID."""
        with app.app_context():
            artist = ArtistService.get_artist_by_id(sample_artist.id)
            
            assert artist is not None
            assert artist.id == sample_artist.id
            assert artist.name == sample_artist.name
    
    def test_get_artist_by_id_not_found(self, app):
        """Test getting artist by non-existent ID."""
        with app.app_context():
            artist = ArtistService.get_artist_by_id(999)
            
            assert artist is None
    
    def test_search_artists(self, app, sample_artist):
        """Test searching artists by name."""
        with app.app_context():
            # Test exact match
            response = ArtistService.search_artists('Test Artist')
            assert response['count'] == 1
            assert response['data'][0]['name'] == 'Test Artist'
            
            # Test partial match
            response = ArtistService.search_artists('Test')
            assert response['count'] == 1
            
            # Test case insensitive
            response = ArtistService.search_artists('test artist')
            assert response['count'] == 1
            
            # Test no match
            response = ArtistService.search_artists('NonExistent')
            assert response['count'] == 0
    
    def test_create_artist(self, app, sample_genre):
        """Test creating an artist through service."""
        with app.app_context():
            artist_data = ArtistCreate(
                name='New Artist',
                city='New City',
                state='NC',
                phone='987-654-3210',
                genres=['Rock']
            )
            
            artist = ArtistService.create_artist(artist_data)
            
            assert artist.id is not None
            assert artist.name == 'New Artist'
            assert artist.city == 'New City'
            assert artist.state == 'NC'
            assert len(artist.genres) == 1
    
    def test_update_artist(self, app, sample_artist):
        """Test updating an artist through service."""
        with app.app_context():
            artist_data = ArtistUpdate(
                name='Updated Artist',
                city='Updated City'
            )
            
            updated_artist = ArtistService.update_artist(sample_artist.id, artist_data)
            
            assert updated_artist is not None
            assert updated_artist.name == 'Updated Artist'
            assert updated_artist.city == 'Updated City'
            assert updated_artist.state == sample_artist.state  # Unchanged
    
    def test_delete_artist(self, app, sample_artist):
        """Test deleting an artist through service."""
        with app.app_context():
            artist_id = sample_artist.id
            
            success = ArtistService.delete_artist(artist_id)
            
            assert success is True
            
            # Verify artist is deleted
            artist = ArtistService.get_artist_by_id(artist_id)
            assert artist is None
    
    def test_delete_artist_not_found(self, app):
        """Test deleting non-existent artist."""
        with app.app_context():
            success = ArtistService.delete_artist(999)
            
            assert success is False

"""
Unit tests for schemas.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from app.schemas import (
    VenueCreate, VenueUpdate, VenueResponse, VenueListItem, VenueSearchResponse,
    ArtistCreate, ArtistUpdate, ArtistResponse, ArtistListItem, ArtistSearchResponse,
    ShowCreate, ShowResponse, ShowListItem,
    BaseSchema, TimestampMixin
)


class TestBaseSchema:
    """Test cases for BaseSchema."""
    
    def test_base_schema_config(self):
        """Test base schema configuration."""
        class TestSchema(BaseSchema):
            name: str
        
        schema = TestSchema(name="test")
        assert schema.name == "test"
    
    def test_timestamp_mixin(self):
        """Test timestamp mixin."""
        class TestSchema(TimestampMixin):
            name: str
        
        now = datetime.utcnow()
        schema = TestSchema(name="test", created_at=now)
        assert schema.name == "test"
        assert schema.created_at == now
        assert schema.updated_at is None


class TestVenueSchemas:
    """Test cases for venue schemas."""
    
    def test_venue_create_valid(self):
        """Test valid venue creation."""
        venue_data = {
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'phone': '123-456-7890',
            'image_link': 'https://example.com/image.jpg',
            'facebook_link': 'https://facebook.com/testvenue',
            'website_link': 'https://testvenue.com',
            'genres': ['Rock', 'Jazz'],
            'seeking_talent': True,
            'seeking_description': 'Looking for talent'
        }
        
        venue = VenueCreate(**venue_data)
        assert venue.name == 'Test Venue'
        assert venue.city == 'Test City'
        assert venue.state == 'TC'
        assert venue.address == '123 Test St'
        assert venue.phone == '123-456-7890'
        assert venue.image_link == 'https://example.com/image.jpg'
        assert venue.facebook_link == 'https://facebook.com/testvenue'
        assert venue.website_link == 'https://testvenue.com'
        assert venue.genres == ['Rock', 'Jazz']
        assert venue.seeking_talent is True
        assert venue.seeking_description == 'Looking for talent'
    
    def test_venue_create_invalid_state(self):
        """Test invalid state code."""
        venue_data = {
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'INVALID',
            'address': '123 Test St',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            VenueCreate(**venue_data)
    
    def test_venue_create_invalid_genres(self):
        """Test invalid genres."""
        venue_data = {
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'genres': ['Invalid Genre']
        }
        
        with pytest.raises(ValidationError):
            VenueCreate(**venue_data)
    
    def test_venue_create_invalid_phone(self):
        """Test invalid phone format."""
        venue_data = {
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'phone': 'invalid-phone',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            VenueCreate(**venue_data)
    
    def test_venue_create_empty_genres(self):
        """Test empty genres list."""
        venue_data = {
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'genres': []
        }
        
        with pytest.raises(ValidationError):
            VenueCreate(**venue_data)
    
    def test_venue_create_min_length_validation(self):
        """Test minimum length validation."""
        venue_data = {
            'name': '',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            VenueCreate(**venue_data)
    
    def test_venue_update_partial(self):
        """Test partial venue update."""
        update_data = {
            'name': 'Updated Venue',
            'phone': '987-654-3210'
        }
        
        venue = VenueUpdate(**update_data)
        assert venue.name == 'Updated Venue'
        assert venue.phone == '987-654-3210'
        assert venue.city is None
        assert venue.state is None
        assert venue.address is None
    
    def test_venue_response(self):
        """Test venue response schema."""
        now = datetime.utcnow()
        response_data = {
            'id': 1,
            'name': 'Test Venue',
            'city': 'Test City',
            'state': 'TC',
            'address': '123 Test St',
            'phone': '123-456-7890',
            'image_link': 'https://example.com/image.jpg',
            'facebook_link': 'https://facebook.com/testvenue',
            'website_link': 'https://testvenue.com',
            'genres': ['Rock', 'Jazz'],
            'seeking_talent': True,
            'seeking_description': 'Looking for talent',
            'created_at': now,
            'updated_at': now,
            'num_upcoming_shows': 2,
            'num_past_shows': 1,
            'past_shows': [],
            'upcoming_shows': []
        }
        
        venue = VenueResponse(**response_data)
        assert venue.id == 1
        assert venue.name == 'Test Venue'
        assert venue.num_upcoming_shows == 2
        assert venue.num_past_shows == 1
        assert venue.past_shows == []
        assert venue.upcoming_shows == []
    
    def test_venue_list_item(self):
        """Test venue list item schema."""
        item_data = {
            'id': 1,
            'name': 'Test Venue',
            'num_upcoming_shows': 2
        }
        
        item = VenueListItem(**item_data)
        assert item.id == 1
        assert item.name == 'Test Venue'
        assert item.num_upcoming_shows == 2
    
    def test_venue_search_response(self):
        """Test venue search response schema."""
        response_data = {
            'count': 1,
            'data': [{'id': 1, 'name': 'Test Venue', 'num_upcoming_shows': 2}]
        }
        
        response = VenueSearchResponse(**response_data)
        assert response.count == 1
        assert len(response.data) == 1
        assert response.data[0].id == 1
        assert response.data[0].name == 'Test Venue'


class TestArtistSchemas:
    """Test cases for artist schemas."""
    
    def test_artist_create_valid(self):
        """Test valid artist creation."""
        artist_data = {
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'TC',
            'phone': '123-456-7890',
            'image_link': 'https://example.com/image.jpg',
            'facebook_link': 'https://facebook.com/testartist',
            'website_link': 'https://testartist.com',
            'genres': ['Rock', 'Jazz'],
            'seeking_venue': True,
            'seeking_description': 'Looking for venues'
        }
        
        artist = ArtistCreate(**artist_data)
        assert artist.name == 'Test Artist'
        assert artist.city == 'Test City'
        assert artist.state == 'TC'
        assert artist.phone == '123-456-7890'
        assert artist.image_link == 'https://example.com/image.jpg'
        assert artist.facebook_link == 'https://facebook.com/testartist'
        assert artist.website_link == 'https://testartist.com'
        assert artist.genres == ['Rock', 'Jazz']
        assert artist.seeking_venue is True
        assert artist.seeking_description == 'Looking for venues'
    
    def test_artist_create_invalid_state(self):
        """Test invalid state code."""
        artist_data = {
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'INVALID',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            ArtistCreate(**artist_data)
    
    def test_artist_create_invalid_genres(self):
        """Test invalid genres."""
        artist_data = {
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'TC',
            'genres': ['Invalid Genre']
        }
        
        with pytest.raises(ValidationError):
            ArtistCreate(**artist_data)
    
    def test_artist_create_invalid_phone(self):
        """Test invalid phone format."""
        artist_data = {
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'TC',
            'phone': 'invalid-phone',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            ArtistCreate(**artist_data)
    
    def test_artist_create_empty_genres(self):
        """Test empty genres list."""
        artist_data = {
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'TC',
            'genres': []
        }
        
        with pytest.raises(ValidationError):
            ArtistCreate(**artist_data)
    
    def test_artist_create_min_length_validation(self):
        """Test minimum length validation."""
        artist_data = {
            'name': '',
            'city': 'Test City',
            'state': 'TC',
            'genres': ['Rock']
        }
        
        with pytest.raises(ValidationError):
            ArtistCreate(**artist_data)
    
    def test_artist_update_partial(self):
        """Test partial artist update."""
        update_data = {
            'name': 'Updated Artist',
            'phone': '987-654-3210'
        }
        
        artist = ArtistUpdate(**update_data)
        assert artist.name == 'Updated Artist'
        assert artist.phone == '987-654-3210'
        assert artist.city is None
        assert artist.state is None
    
    def test_artist_response(self):
        """Test artist response schema."""
        now = datetime.utcnow()
        response_data = {
            'id': 1,
            'name': 'Test Artist',
            'city': 'Test City',
            'state': 'TC',
            'phone': '123-456-7890',
            'image_link': 'https://example.com/image.jpg',
            'facebook_link': 'https://facebook.com/testartist',
            'website_link': 'https://testartist.com',
            'genres': ['Rock', 'Jazz'],
            'seeking_venue': True,
            'seeking_description': 'Looking for venues',
            'created_at': now,
            'updated_at': now,
            'num_upcoming_shows': 2,
            'num_past_shows': 1,
            'past_shows': [],
            'upcoming_shows': []
        }
        
        artist = ArtistResponse(**response_data)
        assert artist.id == 1
        assert artist.name == 'Test Artist'
        assert artist.num_upcoming_shows == 2
        assert artist.num_past_shows == 1
        assert artist.past_shows == []
        assert artist.upcoming_shows == []
    
    def test_artist_list_item(self):
        """Test artist list item schema."""
        item_data = {
            'id': 1,
            'name': 'Test Artist',
            'num_upcoming_shows': 2
        }
        
        item = ArtistListItem(**item_data)
        assert item.id == 1
        assert item.name == 'Test Artist'
        assert item.num_upcoming_shows == 2
    
    def test_artist_search_response(self):
        """Test artist search response schema."""
        response_data = {
            'count': 1,
            'data': [{'id': 1, 'name': 'Test Artist', 'num_upcoming_shows': 2}]
        }
        
        response = ArtistSearchResponse(**response_data)
        assert response.count == 1
        assert len(response.data) == 1
        assert response.data[0].id == 1
        assert response.data[0].name == 'Test Artist'


class TestShowSchemas:
    """Test cases for show schemas."""
    
    def test_show_create_valid(self):
        """Test valid show creation."""
        start_time = datetime.utcnow() + timedelta(days=1)
        show_data = {
            'artist_id': 1,
            'venue_id': 1,
            'start_time': start_time
        }
        
        show = ShowCreate(**show_data)
        assert show.artist_id == 1
        assert show.venue_id == 1
        assert show.start_time == start_time
    
    def test_show_create_invalid_artist_id(self):
        """Test invalid artist ID."""
        start_time = datetime.utcnow() + timedelta(days=1)
        show_data = {
            'artist_id': 0,  # Invalid ID
            'venue_id': 1,
            'start_time': start_time
        }
        
        with pytest.raises(ValidationError):
            ShowCreate(**show_data)
    
    def test_show_create_invalid_venue_id(self):
        """Test invalid venue ID."""
        start_time = datetime.utcnow() + timedelta(days=1)
        show_data = {
            'artist_id': 1,
            'venue_id': 0,  # Invalid ID
            'start_time': start_time
        }
        
        with pytest.raises(ValidationError):
            ShowCreate(**show_data)
    
    def test_show_response(self):
        """Test show response schema."""
        now = datetime.utcnow()
        start_time = now + timedelta(days=1)
        response_data = {
            'id': 1,
            'artist_id': 1,
            'artist_name': 'Test Artist',
            'artist_image_link': 'https://example.com/artist.jpg',
            'venue_id': 1,
            'venue_name': 'Test Venue',
            'venue_image_link': 'https://example.com/venue.jpg',
            'start_time': start_time,
            'created_at': now,
            'updated_at': now
        }
        
        show = ShowResponse(**response_data)
        assert show.id == 1
        assert show.artist_id == 1
        assert show.artist_name == 'Test Artist'
        assert show.artist_image_link == 'https://example.com/artist.jpg'
        assert show.venue_id == 1
        assert show.venue_name == 'Test Venue'
        assert show.venue_image_link == 'https://example.com/venue.jpg'
        assert show.start_time == start_time
    
    def test_show_list_item(self):
        """Test show list item schema."""
        start_time = datetime.utcnow() + timedelta(days=1)
        item_data = {
            'id': 1,
            'venue_id': 1,
            'venue_name': 'Test Venue',
            'artist_id': 1,
            'artist_name': 'Test Artist',
            'start_time': start_time
        }
        
        item = ShowListItem(**item_data)
        assert item.id == 1
        assert item.venue_id == 1
        assert item.venue_name == 'Test Venue'
        assert item.artist_id == 1
        assert item.artist_name == 'Test Artist'
        assert item.start_time == start_time


class TestSchemaValidation:
    """Test cases for schema validation."""
    
    def test_state_code_validation(self):
        """Test state code validation."""
        # Valid state codes
        valid_states = ['CA', 'NY', 'TX', 'FL']
        for state in valid_states:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': state,
                'address': '123 Test St',
                'genres': ['Rock']
            }
            venue = VenueCreate(**venue_data)
            assert venue.state == state
        
        # Invalid state codes
        invalid_states = ['INVALID', 'C', 'CALIFORNIA', 'ca']
        for state in invalid_states:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': state,
                'address': '123 Test St',
                'genres': ['Rock']
            }
            with pytest.raises(ValidationError):
                VenueCreate(**venue_data)
    
    def test_genre_validation(self):
        """Test genre validation."""
        # Valid genres
        valid_genres = ['Rock', 'Jazz', 'Blues', 'Classical', 'Pop']
        for genre in valid_genres:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'genres': [genre]
            }
            venue = VenueCreate(**venue_data)
            assert venue.genres == [genre]
        
        # Invalid genres
        invalid_genres = ['Invalid Genre', 'Rock and Roll', 'Jazz Fusion']
        for genre in invalid_genres:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'genres': [genre]
            }
            with pytest.raises(ValidationError):
                VenueCreate(**venue_data)
    
    def test_phone_validation(self):
        """Test phone validation."""
        # Valid phone formats
        valid_phones = ['123-456-7890', '555-123-4567', '999-888-7777']
        for phone in valid_phones:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'phone': phone,
                'genres': ['Rock']
            }
            venue = VenueCreate(**venue_data)
            assert venue.phone == phone
        
        # Invalid phone formats
        invalid_phones = ['1234567890', '123-456-789', '123-456-78901', 'abc-def-ghij']
        for phone in invalid_phones:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'phone': phone,
                'genres': ['Rock']
            }
            with pytest.raises(ValidationError):
                VenueCreate(**venue_data)
    
    def test_url_validation(self):
        """Test URL validation."""
        # Valid URLs
        valid_urls = [
            'https://example.com',
            'http://example.com',
            'https://www.example.com/path',
            'https://example.com:8080/path?query=value'
        ]
        for url in valid_urls:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'image_link': url,
                'genres': ['Rock']
            }
            venue = VenueCreate(**venue_data)
            assert venue.image_link == url
        
        # Invalid URLs
        invalid_urls = ['not-a-url', 'ftp://example.com', 'example.com']
        for url in invalid_urls:
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'CA',
                'address': '123 Test St',
                'image_link': url,
                'genres': ['Rock']
            }
            with pytest.raises(ValidationError):
                VenueCreate(**venue_data)

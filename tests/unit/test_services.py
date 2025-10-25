"""
Unit tests for services.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre
from app.services import VenueService, ArtistService, ShowService, GenreService
from app.schemas import VenueCreate, VenueUpdate, ArtistCreate, ArtistUpdate, ShowCreate
from app.exceptions import (
    VenueNotFoundException, DuplicateVenueException, DatabaseException,
    ArtistNotFoundException, DuplicateArtistException, ShowNotFoundException,
    ValidationException
)


class TestVenueService:
    """Test cases for VenueService."""
    
    def test_create_venue(self, app, venue_service):
        """Test creating a venue."""
        with app.app_context():
            venue_data = VenueCreate(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent',
                genres=['Rock', 'Jazz']
            )
            
            # Create genres first
            for genre_name in venue_data.genres:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            db.session.commit()
            
            venue = venue_service.create_venue(venue_data)
            
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
            assert venue.state == 'TC'
            assert len(venue.genres) == 2
    
    def test_update_venue(self, app, venue_service, sample_venue):
        """Test updating a venue."""
        with app.app_context():
            update_data = VenueUpdate(
                name='Updated Venue',
                phone='987-654-3210'
            )
            
            updated_venue = venue_service.update_venue(sample_venue.id, update_data)
            
            assert updated_venue is not None
            assert updated_venue.name == 'Updated Venue'
            assert updated_venue.phone == '987-654-3210'
    
    def test_get_venue_with_shows(self, app, venue_service, sample_venue):
        """Test getting venue with shows."""
        with app.app_context():
            venue = venue_service.get_venue_with_shows(sample_venue.id)
            assert venue is not None
            assert venue.name == 'Test Venue'
    
    def test_get_venue_response(self, app, venue_service, sample_venue):
        """Test getting venue response."""
        with app.app_context():
            response = venue_service.get_venue_response(sample_venue.id)
            assert response is not None
            assert response.name == 'Test Venue'
            assert response.city == 'Test City'
            assert response.state == 'TC'
    
    def test_get_venues_by_area(self, app, venue_service, sample_venue):
        """Test getting venues by area."""
        with app.app_context():
            venues = venue_service.get_venues_by_area('Test City', 'TC')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_search_venues(self, app, venue_service, sample_venue):
        """Test searching venues."""
        with app.app_context():
            venues = venue_service.search_venues('Test')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_get_venues_with_counts(self, app, venue_service, sample_venue):
        """Test getting venues with counts."""
        with app.app_context():
            venues = venue_service.get_venues_with_counts()
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_get_areas(self, app, venue_service, sample_venue):
        """Test getting areas."""
        with app.app_context():
            areas = venue_service.get_areas()
            assert len(areas) == 1
            assert areas[0]['city'] == 'Test City'
            assert areas[0]['state'] == 'TC'
    
    def test_delete_venue(self, app, venue_service, sample_venue):
        """Test deleting a venue."""
        with app.app_context():
            success = venue_service.delete_venue(sample_venue.id)
            assert success is True
            
            # Verify venue is deleted
            venue = venue_service.get_by_id(sample_venue.id)
            assert venue is None
    
    def test_delete_venue_with_shows(self, app, venue_service, sample_venue, sample_show):
        """Test deleting venue with shows should fail."""
        with app.app_context():
            with pytest.raises(DatabaseException):
                venue_service.delete_venue(sample_venue.id)
    
    def test_venue_not_found(self, app, venue_service):
        """Test venue not found scenarios."""
        with app.app_context():
            with pytest.raises(VenueNotFoundException):
                venue_service.get_venue_with_shows(999)
            
            with pytest.raises(VenueNotFoundException):
                venue_service.delete_venue(999)


class TestArtistService:
    """Test cases for ArtistService."""
    
    def test_create_artist(self, app, artist_service):
        """Test creating an artist."""
        with app.app_context():
            artist_data = ArtistCreate(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues',
                genres=['Rock', 'Jazz']
            )
            
            # Create genres first
            for genre_name in artist_data.genres:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            db.session.commit()
            
            artist = artist_service.create_artist(artist_data)
            
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
            assert artist.state == 'TC'
            assert len(artist.genres) == 2
    
    def test_update_artist(self, app, artist_service, sample_artist):
        """Test updating an artist."""
        with app.app_context():
            update_data = ArtistUpdate(
                name='Updated Artist',
                phone='987-654-3210'
            )
            
            updated_artist = artist_service.update_artist(sample_artist.id, update_data)
            
            assert updated_artist is not None
            assert updated_artist.name == 'Updated Artist'
            assert updated_artist.phone == '987-654-3210'
    
    def test_get_artist_with_shows(self, app, artist_service, sample_artist):
        """Test getting artist with shows."""
        with app.app_context():
            artist = artist_service.get_artist_with_shows(sample_artist.id)
            assert artist is not None
            assert artist.name == 'Test Artist'
    
    def test_get_artist_response(self, app, artist_service, sample_artist):
        """Test getting artist response."""
        with app.app_context():
            response = artist_service.get_artist_response(sample_artist.id)
            assert response is not None
            assert response.name == 'Test Artist'
            assert response.city == 'Test City'
            assert response.state == 'TC'
    
    def test_get_artists_by_area(self, app, artist_service, sample_artist):
        """Test getting artists by area."""
        with app.app_context():
            artists = artist_service.get_artists_by_area('Test City', 'TC')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_search_artists(self, app, artist_service, sample_artist):
        """Test searching artists."""
        with app.app_context():
            artists = artist_service.search_artists('Test')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_get_artists_with_counts(self, app, artist_service, sample_artist):
        """Test getting artists with counts."""
        with app.app_context():
            artists = artist_service.get_artists_with_counts()
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_delete_artist(self, app, artist_service, sample_artist):
        """Test deleting an artist."""
        with app.app_context():
            success = artist_service.delete_artist(sample_artist.id)
            assert success is True
            
            # Verify artist is deleted
            artist = artist_service.get_by_id(sample_artist.id)
            assert artist is None
    
    def test_delete_artist_with_shows(self, app, artist_service, sample_artist, sample_show):
        """Test deleting artist with shows should fail."""
        with app.app_context():
            with pytest.raises(DatabaseException):
                artist_service.delete_artist(sample_artist.id)
    
    def test_artist_not_found(self, app, artist_service):
        """Test artist not found scenarios."""
        with app.app_context():
            with pytest.raises(ArtistNotFoundException):
                artist_service.get_artist_with_shows(999)
            
            with pytest.raises(ArtistNotFoundException):
                artist_service.delete_artist(999)


class TestShowService:
    """Test cases for ShowService."""
    
    def test_create_show(self, app, show_service, sample_venue, sample_artist):
        """Test creating a show."""
        with app.app_context():
            start_time = datetime.utcnow() + timedelta(days=1)
            show_data = ShowCreate(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=start_time
            )
            
            show = show_service.create_show(show_data)
            
            assert show.artist_id == sample_artist.id
            assert show.venue_id == sample_venue.id
            assert show.start_time == start_time
    
    def test_get_show_response(self, app, show_service, sample_show):
        """Test getting show response."""
        with app.app_context():
            response = show_service.get_show_response(sample_show.id)
            assert response is not None
            assert response.artist_id == sample_show.artist_id
            assert response.venue_id == sample_show.venue_id
    
    def test_get_upcoming_shows(self, app, show_service, sample_show):
        """Test getting upcoming shows."""
        with app.app_context():
            shows = show_service.get_upcoming_shows()
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_past_shows(self, app, show_service):
        """Test getting past shows."""
        with app.app_context():
            # Create a past show
            past_show = Show(
                artist_id=1,
                venue_id=1,
                start_time=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(past_show)
            db.session.commit()
            
            shows = show_service.get_past_shows()
            assert len(shows) == 1
            assert shows[0].id == past_show.id
    
    def test_get_shows_by_artist(self, app, show_service, sample_show):
        """Test getting shows by artist."""
        with app.app_context():
            shows = show_service.get_shows_by_artist(sample_show.artist_id)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_shows_by_venue(self, app, show_service, sample_show):
        """Test getting shows by venue."""
        with app.app_context():
            shows = show_service.get_shows_by_venue(sample_show.venue_id)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_recent_shows(self, app, show_service, sample_show):
        """Test getting recent shows."""
        with app.app_context():
            shows = show_service.get_recent_shows(days=30)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_shows_by_date_range(self, app, show_service, sample_show):
        """Test getting shows by date range."""
        with app.app_context():
            start_date = datetime.utcnow()
            end_date = datetime.utcnow() + timedelta(days=2)
            
            shows = show_service.get_shows_by_date_range(start_date, end_date)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_show_statistics(self, app, show_service, sample_show):
        """Test getting show statistics."""
        with app.app_context():
            stats = show_service.get_show_statistics()
            assert 'total_shows' in stats
            assert 'upcoming_shows' in stats
            assert 'past_shows' in stats
            assert stats['total_shows'] == 1
            assert stats['upcoming_shows'] == 1
            assert stats['past_shows'] == 0
    
    def test_get_shows_list_items(self, app, show_service, sample_show):
        """Test converting shows to list items."""
        with app.app_context():
            shows = [sample_show]
            items = show_service.get_shows_list_items(shows)
            assert len(items) == 1
            assert items[0].id == sample_show.id
            assert items[0].venue_name == sample_show.venue.name
            assert items[0].artist_name == sample_show.artist.name
    
    def test_delete_show(self, app, show_service, sample_show):
        """Test deleting a show."""
        with app.app_context():
            success = show_service.delete_show(sample_show.id)
            assert success is True
            
            # Verify show is deleted
            show = show_service.get_by_id(sample_show.id)
            assert show is None
    
    def test_validate_show_time(self, app, show_service):
        """Test validating show time."""
        with app.app_context():
            # Valid future time
            future_time = datetime.utcnow() + timedelta(days=1)
            show_service.validate_show_time(future_time)  # Should not raise
            
            # Invalid past time
            past_time = datetime.utcnow() - timedelta(days=1)
            with pytest.raises(DatabaseException):
                show_service.validate_show_time(past_time)
    
    def test_show_not_found(self, app, show_service):
        """Test show not found scenarios."""
        with app.app_context():
            with pytest.raises(ShowNotFoundException):
                show_service.get_show_response(999)
            
            with pytest.raises(ShowNotFoundException):
                show_service.delete_show(999)


class TestGenreService:
    """Test cases for GenreService."""
    
    def test_get_genre_by_name(self, app, genre_service, sample_genre):
        """Test getting genre by name."""
        with app.app_context():
            genre = genre_service.get_genre_by_name('Rock')
            assert genre is not None
            assert genre.name == 'Rock'
    
    def test_get_or_create_genre(self, app, genre_service):
        """Test getting or creating genre."""
        with app.app_context():
            genre = genre_service.get_or_create_genre('Jazz')
            assert genre.name == 'Jazz'
            assert genre.id is not None
    
    def test_get_artists_by_genre(self, app, genre_service, sample_genre, sample_artist):
        """Test getting artists by genre."""
        with app.app_context():
            artists = genre_service.get_artists_by_genre('Rock')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_get_venues_by_genre(self, app, genre_service, sample_genre, sample_venue):
        """Test getting venues by genre."""
        with app.app_context():
            venues = genre_service.get_venues_by_genre('Rock')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_get_popular_genres(self, app, genre_service, sample_genre, sample_venue, sample_artist):
        """Test getting popular genres."""
        with app.app_context():
            popular = genre_service.get_popular_genres()
            assert len(popular) == 1
            assert popular[0]['name'] == 'Rock'
            assert popular[0]['artist_count'] == 1
            assert popular[0]['venue_count'] == 1
    
    def test_get_genre_statistics(self, app, genre_service, sample_genre):
        """Test getting genre statistics."""
        with app.app_context():
            stats = genre_service.get_genre_statistics()
            assert 'total_genres' in stats
            assert 'genres_with_artists' in stats
            assert 'genres_with_venues' in stats
            assert stats['total_genres'] == 1
    
    def test_search_genres(self, app, genre_service, sample_genre):
        """Test searching genres."""
        with app.app_context():
            genres = genre_service.search_genres('Rock')
            assert len(genres) == 1
            assert genres[0].name == 'Rock'
    
    def test_get_all_genre_names(self, app, genre_service, sample_genre):
        """Test getting all genre names."""
        with app.app_context():
            names = genre_service.get_all_genre_names()
            assert 'Rock' in names
            assert len(names) == 1
    
    def test_validate_genres(self, app, genre_service, sample_genre):
        """Test validating genres."""
        with app.app_context():
            genres = genre_service.validate_genres(['Rock'])
            assert len(genres) == 1
            assert genres[0].name == 'Rock'
    
    def test_validate_invalid_genres(self, app, genre_service):
        """Test validating invalid genres."""
        with app.app_context():
            with pytest.raises(DatabaseException):
                genre_service.validate_genres(['Invalid Genre'])
    
    def test_create_multiple_genres(self, app, genre_service):
        """Test creating multiple genres."""
        with app.app_context():
            genres = genre_service.create_multiple_genres(['Jazz', 'Blues'])
            assert len(genres) == 2
            assert genres[0].name in ['Jazz', 'Blues']
            assert genres[1].name in ['Jazz', 'Blues']
    
    def test_get_genre_usage_stats(self, app, genre_service, sample_genre, sample_venue, sample_artist):
        """Test getting genre usage stats."""
        with app.app_context():
            stats = genre_service.get_genre_usage_stats()
            assert 'summary' in stats
            assert 'top_genres' in stats
            assert 'total_genres' in stats
            assert stats['total_genres'] == 1
    
    def test_ensure_default_genres(self, app, genre_service):
        """Test ensuring default genres exist."""
        with app.app_context():
            genres = genre_service.ensure_default_genres()
            assert len(genres) > 0
            assert any(genre.name == 'Rock' for genre in genres)
    
    def test_delete_unused_genres(self, app, genre_service):
        """Test deleting unused genres."""
        with app.app_context():
            # Create an unused genre
            unused_genre = Genre(name='Unused Genre')
            db.session.add(unused_genre)
            db.session.commit()
            
            count = genre_service.delete_unused_genres()
            assert count == 1
            
            # Verify genre is deleted
            genre = genre_service.get_genre_by_name('Unused Genre')
            assert genre is None

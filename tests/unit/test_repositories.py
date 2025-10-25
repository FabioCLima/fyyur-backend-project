"""
Unit tests for repositories.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre
from app.repositories import VenueRepository, ArtistRepository, ShowRepository, GenreRepository
from app.exceptions import DatabaseException, DuplicateVenueException, DuplicateArtistException


class TestVenueRepository:
    """Test cases for VenueRepository."""
    
    def test_create_venue(self, app, venue_repository):
        """Test creating a venue."""
        with app.app_context():
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'TC',
                'address': '123 Test St',
                'phone': '123-456-7890',
                'seeking_talent': True,
                'seeking_description': 'Looking for talent'
            }
            genres = ['Rock', 'Jazz']
            
            # Create genres first
            for genre_name in genres:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            db.session.commit()
            
            venue = venue_repository.create_with_genres(venue_data, genres)
            
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
            assert venue.state == 'TC'
            assert len(venue.genres) == 2
            assert venue.genres[0].name in genres
    
    def test_get_by_name_and_city(self, app, venue_repository, sample_venue):
        """Test getting venue by name and city."""
        with app.app_context():
            venue = venue_repository.get_by_name_and_city('Test Venue', 'Test City')
            assert venue is not None
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
    
    def test_get_by_city_state(self, app, venue_repository, sample_venue):
        """Test getting venues by city and state."""
        with app.app_context():
            venues = venue_repository.get_by_city_state('Test City', 'TC')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_search_by_name(self, app, venue_repository, sample_venue):
        """Test searching venues by name."""
        with app.app_context():
            venues = venue_repository.search_by_name('Test')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_duplicate_venue_creation(self, app, venue_repository, sample_venue):
        """Test that duplicate venue creation raises exception."""
        with app.app_context():
            venue_data = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'TC',
                'address': '123 Test St',
                'phone': '123-456-7890',
                'seeking_talent': True,
                'seeking_description': 'Looking for talent'
            }
            genres = ['Rock']
            
            with pytest.raises(DuplicateVenueException):
                venue_repository.create_with_genres(venue_data, genres)


class TestArtistRepository:
    """Test cases for ArtistRepository."""
    
    def test_create_artist(self, app, artist_repository):
        """Test creating an artist."""
        with app.app_context():
            artist_data = {
                'name': 'Test Artist',
                'city': 'Test City',
                'state': 'TC',
                'phone': '123-456-7890',
                'seeking_venue': True,
                'seeking_description': 'Looking for venues'
            }
            genres = ['Rock', 'Jazz']
            
            # Create genres first
            for genre_name in genres:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            db.session.commit()
            
            artist = artist_repository.create_with_genres(artist_data, genres)
            
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
            assert artist.state == 'TC'
            assert len(artist.genres) == 2
            assert artist.genres[0].name in genres
    
    def test_get_by_name_and_city(self, app, artist_repository, sample_artist):
        """Test getting artist by name and city."""
        with app.app_context():
            artist = artist_repository.get_by_name_and_city('Test Artist', 'Test City')
            assert artist is not None
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
    
    def test_get_by_city_state(self, app, artist_repository, sample_artist):
        """Test getting artists by city and state."""
        with app.app_context():
            artists = artist_repository.get_by_city_state('Test City', 'TC')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_search_by_name(self, app, artist_repository, sample_artist):
        """Test searching artists by name."""
        with app.app_context():
            artists = artist_repository.search_by_name('Test')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_duplicate_artist_creation(self, app, artist_repository, sample_artist):
        """Test that duplicate artist creation raises exception."""
        with app.app_context():
            artist_data = {
                'name': 'Test Artist',
                'city': 'Test City',
                'state': 'TC',
                'phone': '123-456-7890',
                'seeking_venue': True,
                'seeking_description': 'Looking for venues'
            }
            genres = ['Rock']
            
            with pytest.raises(DuplicateArtistException):
                artist_repository.create_with_genres(artist_data, genres)


class TestShowRepository:
    """Test cases for ShowRepository."""
    
    def test_create_show(self, app, show_repository, sample_venue, sample_artist):
        """Test creating a show."""
        with app.app_context():
            start_time = datetime.utcnow() + timedelta(days=1)
            show = show_repository.create_with_validation(
                sample_artist.id,
                sample_venue.id,
                start_time
            )
            
            assert show.artist_id == sample_artist.id
            assert show.venue_id == sample_venue.id
            assert show.start_time == start_time
    
    def test_get_by_artist_and_time(self, app, show_repository, sample_show):
        """Test getting show by artist and time."""
        with app.app_context():
            show = show_repository.get_by_artist_and_time(
                sample_show.artist_id,
                sample_show.start_time
            )
            assert show is not None
            assert show.id == sample_show.id
    
    def test_get_by_venue_and_time(self, app, show_repository, sample_show):
        """Test getting show by venue and time."""
        with app.app_context():
            show = show_repository.get_by_venue_and_time(
                sample_show.venue_id,
                sample_show.start_time
            )
            assert show is not None
            assert show.id == sample_show.id
    
    def test_get_upcoming_shows(self, app, show_repository, sample_show):
        """Test getting upcoming shows."""
        with app.app_context():
            shows = show_repository.get_upcoming_shows()
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_past_shows(self, app, show_repository):
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
            
            shows = show_repository.get_past_shows()
            assert len(shows) == 1
            assert shows[0].id == past_show.id
    
    def test_get_shows_by_artist(self, app, show_repository, sample_show):
        """Test getting shows by artist."""
        with app.app_context():
            shows = show_repository.get_shows_by_artist(sample_show.artist_id)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_shows_by_venue(self, app, show_repository, sample_show):
        """Test getting shows by venue."""
        with app.app_context():
            shows = show_repository.get_shows_by_venue(sample_show.venue_id)
            assert len(shows) == 1
            assert shows[0].id == sample_show.id
    
    def test_get_show_statistics(self, app, show_repository, sample_show):
        """Test getting show statistics."""
        with app.app_context():
            stats = show_repository.get_show_statistics()
            assert 'total_shows' in stats
            assert 'upcoming_shows' in stats
            assert 'past_shows' in stats
            assert stats['total_shows'] == 1
            assert stats['upcoming_shows'] == 1
            assert stats['past_shows'] == 0


class TestGenreRepository:
    """Test cases for GenreRepository."""
    
    def test_create_genre(self, app, genre_repository):
        """Test creating a genre."""
        with app.app_context():
            genre = genre_repository.get_or_create('Test Genre')
            assert genre.name == 'Test Genre'
    
    def test_get_by_name(self, app, genre_repository, sample_genre):
        """Test getting genre by name."""
        with app.app_context():
            genre = genre_repository.get_by_name('Rock')
            assert genre is not None
            assert genre.name == 'Rock'
    
    def test_get_or_create_existing(self, app, genre_repository, sample_genre):
        """Test getting existing genre."""
        with app.app_context():
            genre = genre_repository.get_or_create('Rock')
            assert genre.name == 'Rock'
            assert genre.id == sample_genre.id
    
    def test_get_or_create_new(self, app, genre_repository):
        """Test creating new genre."""
        with app.app_context():
            genre = genre_repository.get_or_create('Jazz')
            assert genre.name == 'Jazz'
            assert genre.id is not None
    
    def test_get_artists_by_genre(self, app, genre_repository, sample_genre, sample_artist):
        """Test getting artists by genre."""
        with app.app_context():
            artists = genre_repository.get_artists_by_genre('Rock')
            assert len(artists) == 1
            assert artists[0].name == 'Test Artist'
    
    def test_get_venues_by_genre(self, app, genre_repository, sample_genre, sample_venue):
        """Test getting venues by genre."""
        with app.app_context():
            venues = genre_repository.get_venues_by_genre('Rock')
            assert len(venues) == 1
            assert venues[0].name == 'Test Venue'
    
    def test_get_popular_genres(self, app, genre_repository, sample_genre, sample_venue, sample_artist):
        """Test getting popular genres."""
        with app.app_context():
            popular = genre_repository.get_popular_genres()
            assert len(popular) == 1
            assert popular[0]['name'] == 'Rock'
            assert popular[0]['artist_count'] == 1
            assert popular[0]['venue_count'] == 1
    
    def test_get_genre_statistics(self, app, genre_repository, sample_genre):
        """Test getting genre statistics."""
        with app.app_context():
            stats = genre_repository.get_genre_statistics()
            assert 'total_genres' in stats
            assert 'genres_with_artists' in stats
            assert 'genres_with_venues' in stats
            assert stats['total_genres'] == 1
    
    def test_search_by_name(self, app, genre_repository, sample_genre):
        """Test searching genres by name."""
        with app.app_context():
            genres = genre_repository.search_by_name('Rock')
            assert len(genres) == 1
            assert genres[0].name == 'Rock'
    
    def test_get_all_names(self, app, genre_repository, sample_genre):
        """Test getting all genre names."""
        with app.app_context():
            names = genre_repository.get_all_names()
            assert 'Rock' in names
            assert len(names) == 1
    
    def test_validate_genres(self, app, genre_repository, sample_genre):
        """Test validating genres."""
        with app.app_context():
            genres = genre_repository.validate_genres(['Rock'])
            assert len(genres) == 1
            assert genres[0].name == 'Rock'
    
    def test_validate_invalid_genres(self, app, genre_repository):
        """Test validating invalid genres."""
        with app.app_context():
            with pytest.raises(DatabaseException):
                genre_repository.validate_genres(['Invalid Genre'])
    
    def test_create_multiple_genres(self, app, genre_repository):
        """Test creating multiple genres."""
        with app.app_context():
            genres = genre_repository.create_multiple(['Jazz', 'Blues'])
            assert len(genres) == 2
            assert genres[0].name in ['Jazz', 'Blues']
            assert genres[1].name in ['Jazz', 'Blues']

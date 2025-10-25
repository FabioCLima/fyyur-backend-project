"""
Integration tests for the Fyyur application.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre
from app.services import VenueService, ArtistService, ShowService, GenreService
from app.schemas import VenueCreate, ArtistCreate, ShowCreate
from app.exceptions import (
    VenueNotFoundException, DuplicateVenueException, DatabaseException,
    ArtistNotFoundException, DuplicateArtistException, ShowNotFoundException,
    ValidationException
)


class TestVenueIntegration:
    """Integration tests for venue operations."""
    
    def test_create_venue_with_genres(self, app):
        """Test creating a venue with genres."""
        with app.app_context():
            venue_service = VenueService()
            
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Create venue
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
            
            venue = venue_service.create_venue(venue_data)
            
            # Verify venue was created
            assert venue.id is not None
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
            assert venue.state == 'TC'
            assert len(venue.genres) == 2
            assert any(genre.name == 'Rock' for genre in venue.genres)
            assert any(genre.name == 'Jazz' for genre in venue.genres)
    
    def test_venue_crud_operations(self, app):
        """Test complete CRUD operations for venues."""
        with app.app_context():
            venue_service = VenueService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create venue
            venue_data = VenueCreate(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent',
                genres=['Rock']
            )
            
            venue = venue_service.create_venue(venue_data)
            venue_id = venue.id
            
            # Read venue
            retrieved_venue = venue_service.get_by_id(venue_id)
            assert retrieved_venue is not None
            assert retrieved_venue.name == 'Test Venue'
            
            # Update venue
            from app.schemas import VenueUpdate
            update_data = VenueUpdate(
                name='Updated Venue',
                phone='987-654-3210'
            )
            
            updated_venue = venue_service.update_venue(venue_id, update_data)
            assert updated_venue is not None
            assert updated_venue.name == 'Updated Venue'
            assert updated_venue.phone == '987-654-3210'
            
            # Delete venue
            success = venue_service.delete_venue(venue_id)
            assert success is True
            
            # Verify venue is deleted
            deleted_venue = venue_service.get_by_id(venue_id)
            assert deleted_venue is None
    
    def test_venue_search_and_filtering(self, app):
        """Test venue search and filtering operations."""
        with app.app_context():
            venue_service = VenueService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Create multiple venues
            venues_data = [
                VenueCreate(
                    name='Rock Venue',
                    city='Rock City',
                    state='RC',
                    address='123 Rock St',
                    phone='123-456-7890',
                    seeking_talent=True,
                    seeking_description='Looking for rock talent',
                    genres=['Rock']
                ),
                VenueCreate(
                    name='Jazz Venue',
                    city='Jazz City',
                    state='JC',
                    address='456 Jazz St',
                    phone='987-654-3210',
                    seeking_talent=False,
                    seeking_description='',
                    genres=['Jazz']
                ),
                VenueCreate(
                    name='Mixed Venue',
                    city='Mixed City',
                    state='MC',
                    address='789 Mixed St',
                    phone='555-123-4567',
                    seeking_talent=True,
                    seeking_description='Looking for mixed talent',
                    genres=['Rock', 'Jazz']
                )
            ]
            
            for venue_data in venues_data:
                venue_service.create_venue(venue_data)
            
            # Test search by name
            rock_venues = venue_service.search_venues('Rock')
            assert len(rock_venues) == 2  # Rock Venue and Mixed Venue
            
            # Test search by city
            jazz_venues = venue_service.search_venues('Jazz')
            assert len(jazz_venues) == 2  # Jazz Venue and Mixed Venue
            
            # Test get by area
            rock_city_venues = venue_service.get_venues_by_area('Rock City', 'RC')
            assert len(rock_city_venues) == 1
            assert rock_city_venues[0].name == 'Rock Venue'
            
            # Test get areas
            areas = venue_service.get_areas()
            assert len(areas) == 3
            area_names = [f"{area['city']}, {area['state']}" for area in areas]
            assert 'Rock City, RC' in area_names
            assert 'Jazz City, JC' in area_names
            assert 'Mixed City, MC' in area_names


class TestArtistIntegration:
    """Integration tests for artist operations."""
    
    def test_create_artist_with_genres(self, app):
        """Test creating an artist with genres."""
        with app.app_context():
            artist_service = ArtistService()
            
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Create artist
            artist_data = ArtistCreate(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues',
                genres=['Rock', 'Jazz']
            )
            
            artist = artist_service.create_artist(artist_data)
            
            # Verify artist was created
            assert artist.id is not None
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
            assert artist.state == 'TC'
            assert len(artist.genres) == 2
            assert any(genre.name == 'Rock' for genre in artist.genres)
            assert any(genre.name == 'Jazz' for genre in artist.genres)
    
    def test_artist_crud_operations(self, app):
        """Test complete CRUD operations for artists."""
        with app.app_context():
            artist_service = ArtistService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create artist
            artist_data = ArtistCreate(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues',
                genres=['Rock']
            )
            
            artist = artist_service.create_artist(artist_data)
            artist_id = artist.id
            
            # Read artist
            retrieved_artist = artist_service.get_by_id(artist_id)
            assert retrieved_artist is not None
            assert retrieved_artist.name == 'Test Artist'
            
            # Update artist
            from app.schemas import ArtistUpdate
            update_data = ArtistUpdate(
                name='Updated Artist',
                phone='987-654-3210'
            )
            
            updated_artist = artist_service.update_artist(artist_id, update_data)
            assert updated_artist is not None
            assert updated_artist.name == 'Updated Artist'
            assert updated_artist.phone == '987-654-3210'
            
            # Delete artist
            success = artist_service.delete_artist(artist_id)
            assert success is True
            
            # Verify artist is deleted
            deleted_artist = artist_service.get_by_id(artist_id)
            assert deleted_artist is None
    
    def test_artist_search_and_filtering(self, app):
        """Test artist search and filtering operations."""
        with app.app_context():
            artist_service = ArtistService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Create multiple artists
            artists_data = [
                ArtistCreate(
                    name='Rock Artist',
                    city='Rock City',
                    state='RC',
                    phone='123-456-7890',
                    seeking_venue=True,
                    seeking_description='Looking for rock venues',
                    genres=['Rock']
                ),
                ArtistCreate(
                    name='Jazz Artist',
                    city='Jazz City',
                    state='JC',
                    phone='987-654-3210',
                    seeking_venue=False,
                    seeking_description='',
                    genres=['Jazz']
                ),
                ArtistCreate(
                    name='Mixed Artist',
                    city='Mixed City',
                    state='MC',
                    phone='555-123-4567',
                    seeking_venue=True,
                    seeking_description='Looking for mixed venues',
                    genres=['Rock', 'Jazz']
                )
            ]
            
            for artist_data in artists_data:
                artist_service.create_artist(artist_data)
            
            # Test search by name
            rock_artists = artist_service.search_artists('Rock')
            assert len(rock_artists) == 2  # Rock Artist and Mixed Artist
            
            # Test search by city
            jazz_artists = artist_service.search_artists('Jazz')
            assert len(jazz_artists) == 2  # Jazz Artist and Mixed Artist
            
            # Test get by area
            rock_city_artists = artist_service.get_artists_by_area('Rock City', 'RC')
            assert len(rock_city_artists) == 1
            assert rock_city_artists[0].name == 'Rock Artist'


class TestShowIntegration:
    """Integration tests for show operations."""
    
    def test_create_show_with_validation(self, app):
        """Test creating a show with validation."""
        with app.app_context():
            show_service = ShowService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create venue and artist
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent'
            )
            venue.genres.append(rock_genre)
            
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues'
            )
            artist.genres.append(rock_genre)
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.commit()
            
            # Create show
            start_time = datetime.utcnow() + timedelta(days=1)
            show_data = ShowCreate(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=start_time
            )
            
            show = show_service.create_show(show_data)
            
            # Verify show was created
            assert show.id is not None
            assert show.artist_id == artist.id
            assert show.venue_id == venue.id
            assert show.start_time == start_time
    
    def test_show_crud_operations(self, app):
        """Test complete CRUD operations for shows."""
        with app.app_context():
            show_service = ShowService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create venue and artist
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent'
            )
            venue.genres.append(rock_genre)
            
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues'
            )
            artist.genres.append(rock_genre)
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.commit()
            
            # Create show
            start_time = datetime.utcnow() + timedelta(days=1)
            show_data = ShowCreate(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=start_time
            )
            
            show = show_service.create_show(show_data)
            show_id = show.id
            
            # Read show
            retrieved_show = show_service.get_by_id(show_id)
            assert retrieved_show is not None
            assert retrieved_show.artist_id == artist.id
            assert retrieved_show.venue_id == venue.id
            
            # Delete show
            success = show_service.delete_show(show_id)
            assert success is True
            
            # Verify show is deleted
            deleted_show = show_service.get_by_id(show_id)
            assert deleted_show is None
    
    def test_show_filtering_and_statistics(self, app):
        """Test show filtering and statistics operations."""
        with app.app_context():
            show_service = ShowService()
            
            # Create genres
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create venue and artist
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent'
            )
            venue.genres.append(rock_genre)
            
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues'
            )
            artist.genres.append(rock_genre)
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.commit()
            
            # Create past show
            past_show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(past_show)
            
            # Create upcoming show
            upcoming_show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            db.session.add(upcoming_show)
            db.session.commit()
            
            # Test get upcoming shows
            upcoming_shows = show_service.get_upcoming_shows()
            assert len(upcoming_shows) == 1
            assert upcoming_shows[0].id == upcoming_show.id
            
            # Test get past shows
            past_shows = show_service.get_past_shows()
            assert len(past_shows) == 1
            assert past_shows[0].id == past_show.id
            
            # Test get shows by artist
            artist_shows = show_service.get_shows_by_artist(artist.id)
            assert len(artist_shows) == 2
            
            # Test get shows by venue
            venue_shows = show_service.get_shows_by_venue(venue.id)
            assert len(venue_shows) == 2
            
            # Test get show statistics
            stats = show_service.get_show_statistics()
            assert stats['total_shows'] == 2
            assert stats['upcoming_shows'] == 1
            assert stats['past_shows'] == 1


class TestGenreIntegration:
    """Integration tests for genre operations."""
    
    def test_genre_crud_operations(self, app):
        """Test complete CRUD operations for genres."""
        with app.app_context():
            genre_service = GenreService()
            
            # Create genre
            genre = genre_service.get_or_create_genre('Rock')
            genre_id = genre.id
            
            # Read genre
            retrieved_genre = genre_service.get_genre_by_name('Rock')
            assert retrieved_genre is not None
            assert retrieved_genre.name == 'Rock'
            
            # Get or create existing genre
            existing_genre = genre_service.get_or_create_genre('Rock')
            assert existing_genre.id == genre_id
            
            # Get or create new genre
            new_genre = genre_service.get_or_create_genre('Jazz')
            assert new_genre.id != genre_id
            assert new_genre.name == 'Jazz'
    
    def test_genre_relationships(self, app):
        """Test genre relationships with venues and artists."""
        with app.app_context():
            genre_service = GenreService()
            
            # Create genres
            rock_genre = genre_service.get_or_create_genre('Rock')
            jazz_genre = genre_service.get_or_create_genre('Jazz')
            
            # Create venue with genres
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent'
            )
            venue.genres.extend([rock_genre, jazz_genre])
            
            # Create artist with genres
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues'
            )
            artist.genres.extend([rock_genre, jazz_genre])
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.commit()
            
            # Test get artists by genre
            rock_artists = genre_service.get_artists_by_genre('Rock')
            assert len(rock_artists) == 1
            assert rock_artists[0].name == 'Test Artist'
            
            # Test get venues by genre
            rock_venues = genre_service.get_venues_by_genre('Rock')
            assert len(rock_venues) == 1
            assert rock_venues[0].name == 'Test Venue'
            
            # Test get popular genres
            popular_genres = genre_service.get_popular_genres()
            assert len(popular_genres) == 2
            assert popular_genres[0]['name'] in ['Rock', 'Jazz']
            assert popular_genres[0]['artist_count'] == 1
            assert popular_genres[0]['venue_count'] == 1
            
            # Test get genre statistics
            stats = genre_service.get_genre_statistics()
            assert stats['total_genres'] == 2
            assert stats['genres_with_artists'] == 2
            assert stats['genres_with_venues'] == 2


class TestCrossEntityIntegration:
    """Integration tests across multiple entities."""
    
    def test_venue_artist_show_workflow(self, app):
        """Test complete workflow from venue/artist creation to show booking."""
        with app.app_context():
            venue_service = VenueService()
            artist_service = ArtistService()
            show_service = ShowService()
            genre_service = GenreService()
            
            # Create genres
            rock_genre = genre_service.get_or_create_genre('Rock')
            jazz_genre = genre_service.get_or_create_genre('Jazz')
            
            # Create venue
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
            
            venue = venue_service.create_venue(venue_data)
            
            # Create artist
            artist_data = ArtistCreate(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues',
                genres=['Rock', 'Jazz']
            )
            
            artist = artist_service.create_artist(artist_data)
            
            # Book a show
            start_time = datetime.utcnow() + timedelta(days=1)
            show_data = ShowCreate(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=start_time
            )
            
            show = show_service.create_show(show_data)
            
            # Verify the complete workflow
            assert venue.id is not None
            assert artist.id is not None
            assert show.id is not None
            assert show.artist_id == artist.id
            assert show.venue_id == venue.id
            
            # Verify relationships
            assert len(venue.genres) == 2
            assert len(artist.genres) == 2
            assert len(venue.shows.all()) == 1
            assert len(artist.shows.all()) == 1
            
            # Verify show details
            assert venue.shows.first().artist.name == 'Test Artist'
            assert artist.shows.first().venue.name == 'Test Venue'
    
    def test_data_consistency_across_entities(self, app):
        """Test data consistency across different entities."""
        with app.app_context():
            venue_service = VenueService()
            artist_service = ArtistService()
            show_service = ShowService()
            genre_service = GenreService()
            
            # Create genres
            rock_genre = genre_service.get_or_create_genre('Rock')
            jazz_genre = genre_service.get_or_create_genre('Jazz')
            
            # Create venue
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
            
            venue = venue_service.create_venue(venue_data)
            
            # Create artist
            artist_data = ArtistCreate(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues',
                genres=['Rock', 'Jazz']
            )
            
            artist = artist_service.create_artist(artist_data)
            
            # Book multiple shows
            shows_data = [
                ShowCreate(
                    artist_id=artist.id,
                    venue_id=venue.id,
                    start_time=datetime.utcnow() + timedelta(days=1)
                ),
                ShowCreate(
                    artist_id=artist.id,
                    venue_id=venue.id,
                    start_time=datetime.utcnow() + timedelta(days=7)
                ),
                ShowCreate(
                    artist_id=artist.id,
                    venue_id=venue.id,
                    start_time=datetime.utcnow() + timedelta(days=14)
                )
            ]
            
            for show_data in shows_data:
                show_service.create_show(show_data)
            
            # Verify data consistency
            assert len(venue.shows.all()) == 3
            assert len(artist.shows.all()) == 3
            
            # Verify genre relationships
            assert len(venue.genres) == 2
            assert len(artist.genres) == 2
            
            # Verify show statistics
            stats = show_service.get_show_statistics()
            assert stats['total_shows'] == 3
            assert stats['upcoming_shows'] == 3
            assert stats['past_shows'] == 0
            
            # Verify venue and artist show counts
            venue_response = venue_service.get_venue_response(venue.id)
            assert venue_response.num_upcoming_shows == 3
            assert venue_response.num_past_shows == 0
            
            artist_response = artist_service.get_artist_response(artist.id)
            assert artist_response.num_upcoming_shows == 3
            assert artist_response.num_past_shows == 0

"""
Unit tests for models.
"""
import pytest  # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre
from app.exceptions import DatabaseException


class TestGenreModel:
    """Test cases for Genre model."""
    
    def test_create_genre(self, app):
        """Test creating a genre."""
        with app.app_context():
            genre = Genre(name='Rock')
            db.session.add(genre)
            db.session.commit()
            
            assert genre.id is not None
            assert genre.name == 'Rock'
            assert genre.created_at is not None
            assert genre.updated_at is not None
    
    def test_genre_repr(self, app):
        """Test genre string representation."""
        with app.app_context():
            genre = Genre(name='Rock')
            assert repr(genre) == '<Genre Rock>'
    
    def test_genre_to_dict(self, app):
        """Test genre to dictionary conversion."""
        with app.app_context():
            genre = Genre(name='Rock')
            db.session.add(genre)
            db.session.commit()
            
            genre_dict = genre.to_dict()
            assert genre_dict['id'] == genre.id
            assert genre_dict['name'] == 'Rock'
            assert 'created_at' in genre_dict
            assert 'updated_at' in genre_dict
    
    def test_genre_unique_name(self, app):
        """Test genre name uniqueness."""
        with app.app_context():
            genre1 = Genre(name='Rock')
            genre2 = Genre(name='Rock')
            
            db.session.add(genre1)
            db.session.commit()
            
            db.session.add(genre2)
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()


class TestVenueModel:
    """Test cases for Venue model."""
    
    def test_create_venue(self, app, sample_genre):
        """Test creating a venue."""
        with app.app_context():
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TC',
                address='123 Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for talent'
            )
            venue.genres.append(sample_genre)
            
            db.session.add(venue)
            db.session.commit()
            
            assert venue.id is not None
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
            assert venue.state == 'TC'
            assert venue.address == '123 Test St'
            assert venue.phone == '123-456-7890'
            assert venue.seeking_talent is True
            assert venue.seeking_description == 'Looking for talent'
            assert len(venue.genres) == 1
            assert venue.genres[0].name == 'Rock'
    
    def test_venue_repr(self, app, sample_venue):
        """Test venue string representation."""
        with app.app_context():
            assert repr(sample_venue) == '<Venue Test Venue>'
    
    def test_venue_to_dict(self, app, sample_venue):
        """Test venue to dictionary conversion."""
        with app.app_context():
            venue_dict = sample_venue.to_dict()
            assert venue_dict['id'] == sample_venue.id
            assert venue_dict['name'] == 'Test Venue'
            assert venue_dict['city'] == 'Test City'
            assert venue_dict['state'] == 'TC'
            assert venue_dict['address'] == '123 Test St'
            assert venue_dict['phone'] == '123-456-7890'
            assert venue_dict['seeking_talent'] is True
            assert venue_dict['seeking_description'] == 'Looking for talent'
            assert 'created_at' in venue_dict
            assert 'updated_at' in venue_dict
    
    def test_venue_genres_relationship(self, app, sample_venue, sample_genre):
        """Test venue genres relationship."""
        with app.app_context():
            assert len(sample_venue.genres) == 1
            assert sample_venue.genres[0].name == 'Rock'
            
            # Add another genre
            jazz_genre = Genre(name='Jazz')
            db.session.add(jazz_genre)
            sample_venue.genres.append(jazz_genre)
            db.session.commit()
            
            assert len(sample_venue.genres) == 2
            assert any(genre.name == 'Rock' for genre in sample_venue.genres)
            assert any(genre.name == 'Jazz' for genre in sample_venue.genres)
    
    def test_venue_shows_relationship(self, app, sample_venue, sample_show):
        """Test venue shows relationship."""
        with app.app_context():
            assert len(sample_venue.shows.all()) == 1
            assert sample_venue.shows.first().id == sample_show.id
    
    def test_venue_constraints(self, app):
        """Test venue constraints."""
        with app.app_context():
            # Test unique constraint on name and city
            venue1 = Venue(name='Same Venue', city='Same City', state='SC')
            venue2 = Venue(name='Same Venue', city='Same City', state='SC')
            
            db.session.add(venue1)
            db.session.commit()
            
            db.session.add(venue2)
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()


class TestArtistModel:
    """Test cases for Artist model."""
    
    def test_create_artist(self, app, sample_genre):
        """Test creating an artist."""
        with app.app_context():
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TC',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for venues'
            )
            artist.genres.append(sample_genre)
            
            db.session.add(artist)
            db.session.commit()
            
            assert artist.id is not None
            assert artist.name == 'Test Artist'
            assert artist.city == 'Test City'
            assert artist.state == 'TC'
            assert artist.phone == '123-456-7890'
            assert artist.seeking_venue is True
            assert artist.seeking_description == 'Looking for venues'
            assert len(artist.genres) == 1
            assert artist.genres[0].name == 'Rock'
    
    def test_artist_repr(self, app, sample_artist):
        """Test artist string representation."""
        with app.app_context():
            assert repr(sample_artist) == '<Artist Test Artist>'
    
    def test_artist_to_dict(self, app, sample_artist):
        """Test artist to dictionary conversion."""
        with app.app_context():
            artist_dict = sample_artist.to_dict()
            assert artist_dict['id'] == sample_artist.id
            assert artist_dict['name'] == 'Test Artist'
            assert artist_dict['city'] == 'Test City'
            assert artist_dict['state'] == 'TC'
            assert artist_dict['phone'] == '123-456-7890'
            assert artist_dict['seeking_venue'] is True
            assert artist_dict['seeking_description'] == 'Looking for venues'
            assert 'created_at' in artist_dict
            assert 'updated_at' in artist_dict
    
    def test_artist_genres_relationship(self, app, sample_artist, sample_genre):
        """Test artist genres relationship."""
        with app.app_context():
            assert len(sample_artist.genres) == 1
            assert sample_artist.genres[0].name == 'Rock'
            
            # Add another genre
            jazz_genre = Genre(name='Jazz')
            db.session.add(jazz_genre)
            sample_artist.genres.append(jazz_genre)
            db.session.commit()
            
            assert len(sample_artist.genres) == 2
            assert any(genre.name == 'Rock' for genre in sample_artist.genres)
            assert any(genre.name == 'Jazz' for genre in sample_artist.genres)
    
    def test_artist_shows_relationship(self, app, sample_artist, sample_show):
        """Test artist shows relationship."""
        with app.app_context():
            assert len(sample_artist.shows.all()) == 1
            assert sample_artist.shows.first().id == sample_show.id


class TestShowModel:
    """Test cases for Show model."""
    
    def test_create_show(self, app, sample_venue, sample_artist):
        """Test creating a show."""
        with app.app_context():
            start_time = datetime.utcnow() + timedelta(days=1)
            show = Show(
                artist_id=sample_artist.id,
                venue_id=sample_venue.id,
                start_time=start_time
            )
            
            db.session.add(show)
            db.session.commit()
            
            assert show.id is not None
            assert show.artist_id == sample_artist.id
            assert show.venue_id == sample_venue.id
            assert show.start_time == start_time
            assert show.created_at is not None
            assert show.updated_at is not None
    
    def test_show_repr(self, app, sample_show):
        """Test show string representation."""
        with app.app_context():
            expected_repr = f'<Show {sample_show.artist.name} at {sample_show.venue.name}>'
            assert repr(sample_show) == expected_repr
    
    def test_show_to_dict(self, app, sample_show):
        """Test show to dictionary conversion."""
        with app.app_context():
            show_dict = sample_show.to_dict()
            assert show_dict['id'] == sample_show.id
            assert show_dict['artist_id'] == sample_show.artist_id
            assert show_dict['artist_name'] == sample_show.artist.name
            assert show_dict['venue_id'] == sample_show.venue_id
            assert show_dict['venue_name'] == sample_show.venue.name
            assert show_dict['start_time'] == sample_show.start_time.isoformat()
            assert 'created_at' in show_dict
            assert 'updated_at' in show_dict
    
    def test_show_artist_relationship(self, app, sample_show, sample_artist):
        """Test show artist relationship."""
        with app.app_context():
            assert sample_show.artist.id == sample_artist.id
            assert sample_show.artist.name == sample_artist.name
    
    def test_show_venue_relationship(self, app, sample_show, sample_venue):
        """Test show venue relationship."""
        with app.app_context():
            assert sample_show.venue.id == sample_venue.id
            assert sample_show.venue.name == sample_venue.name
    
    def test_show_constraints(self, app, sample_artist, sample_venue):
        """Test show constraints."""
        with app.app_context():
            start_time = datetime.utcnow() + timedelta(days=1)
            
            # Test unique constraint on artist and start time
            show1 = Show(artist_id=sample_artist.id, venue_id=sample_venue.id, start_time=start_time)
            show2 = Show(artist_id=sample_artist.id, venue_id=sample_venue.id, start_time=start_time)
            
            db.session.add(show1)
            db.session.commit()
            
            db.session.add(show2)
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()
    
    def test_show_cascade_delete(self, app, sample_venue, sample_artist):
        """Test show cascade delete."""
        with app.app_context():
            start_time = datetime.utcnow() + timedelta(days=1)
            show = Show(artist_id=sample_artist.id, venue_id=sample_venue.id, start_time=start_time)
            
            db.session.add(show)
            db.session.commit()
            show_id = show.id
            
            # Delete venue should cascade delete show
            db.session.delete(sample_venue)
            db.session.commit()
            
            # Show should be deleted
            deleted_show = Show.query.get(show_id)
            assert deleted_show is None


class TestModelRelationships:
    """Test cases for model relationships."""
    
    def test_genre_venue_relationship(self, app, sample_genre, sample_venue):
        """Test genre venue relationship."""
        with app.app_context():
            assert len(sample_genre.venues) == 1
            assert sample_genre.venues[0].name == 'Test Venue'
    
    def test_genre_artist_relationship(self, app, sample_genre, sample_artist):
        """Test genre artist relationship."""
        with app.app_context():
            assert len(sample_genre.artists) == 1
            assert sample_genre.artists[0].name == 'Test Artist'
    
    def test_venue_artist_through_shows(self, app, sample_venue, sample_artist, sample_show):
        """Test venue artist relationship through shows."""
        with app.app_context():
            # Get artists performing at this venue
            venue_artists = [show.artist for show in sample_venue.shows]
            assert len(venue_artists) == 1
            assert venue_artists[0].name == 'Test Artist'
    
    def test_artist_venue_through_shows(self, app, sample_venue, sample_artist, sample_show):
        """Test artist venue relationship through shows."""
        with app.app_context():
            # Get venues where this artist performs
            artist_venues = [show.venue for show in sample_artist.shows]
            assert len(artist_venues) == 1
            assert artist_venues[0].name == 'Test Venue'
    
    def test_model_timestamps(self, app):
        """Test model timestamps."""
        with app.app_context():
            genre = Genre(name='Test Genre')
            db.session.add(genre)
            db.session.commit()
            
            original_created = genre.created_at
            original_updated = genre.updated_at
            
            # Update the genre
            genre.name = 'Updated Genre'
            db.session.commit()
            
            assert genre.created_at == original_created
            assert genre.updated_at > original_updated

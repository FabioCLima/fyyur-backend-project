"""
Test configuration and fixtures for the Fyyur application.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import create_app
from app.models import db, Venue, Artist, Show, Genre
from app.services import VenueService, ArtistService, ShowService, GenreService
from app.repositories import VenueRepository, ArtistRepository, ShowRepository, GenreRepository


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_genre(app):
    """Create a sample genre for testing."""
    with app.app_context():
        genre = Genre(name='Rock')
        db.session.add(genre)
        db.session.commit()
        return genre


@pytest.fixture
def sample_venue(app, sample_genre):
    """Create a sample venue for testing."""
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
        return venue


@pytest.fixture
def sample_artist(app, sample_genre):
    """Create a sample artist for testing."""
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
        return artist


@pytest.fixture
def sample_show(app, sample_venue, sample_artist):
    """Create a sample show for testing."""
    with app.app_context():
        from datetime import datetime, timedelta
        show = Show(
            artist_id=sample_artist.id,
            venue_id=sample_venue.id,
            start_time=datetime.utcnow() + timedelta(days=1)
        )
        db.session.add(show)
        db.session.commit()
        return show


# Service fixtures
@pytest.fixture
def venue_service():
    """Create a venue service instance."""
    return VenueService()


@pytest.fixture
def artist_service():
    """Create an artist service instance."""
    return ArtistService()


@pytest.fixture
def show_service():
    """Create a show service instance."""
    return ShowService()


@pytest.fixture
def genre_service():
    """Create a genre service instance."""
    return GenreService()


# Repository fixtures
@pytest.fixture
def venue_repository():
    """Create a venue repository instance."""
    return VenueRepository()


@pytest.fixture
def artist_repository():
    """Create an artist repository instance."""
    return ArtistRepository()


@pytest.fixture
def show_repository():
    """Create a show repository instance."""
    return ShowRepository()


@pytest.fixture
def genre_repository():
    """Create a genre repository instance."""
    return GenreRepository()

"""
Test fixtures for the Fyyur application.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre


@pytest.fixture
def sample_genres(app):
    """Create sample genres for testing."""
    with app.app_context():
        genres = [
            Genre(name='Rock'),
            Genre(name='Jazz'),
            Genre(name='Blues'),
            Genre(name='Classical'),
            Genre(name='Pop'),
            Genre(name='Electronic'),
            Genre(name='Folk'),
            Genre(name='Funk'),
            Genre(name='Hip-Hop'),
            Genre(name='Heavy Metal')
        ]
        
        for genre in genres:
            db.session.add(genre)
        db.session.commit()
        
        return genres


@pytest.fixture
def sample_venues(app, sample_genres):
    """Create sample venues for testing."""
    with app.app_context():
        venues = [
            Venue(
                name='Rock Venue',
                city='Rock City',
                state='RC',
                address='123 Rock St',
                phone='123-456-7890',
                image_link='https://example.com/rock-venue.jpg',
                facebook_link='https://facebook.com/rockvenue',
                website_link='https://rockvenue.com',
                seeking_talent=True,
                seeking_description='Looking for rock talent',
                genres=[sample_genres[0]]  # Rock
            ),
            Venue(
                name='Jazz Venue',
                city='Jazz City',
                state='JC',
                address='456 Jazz St',
                phone='987-654-3210',
                image_link='https://example.com/jazz-venue.jpg',
                facebook_link='https://facebook.com/jazzvenue',
                website_link='https://jazzvenue.com',
                seeking_talent=False,
                seeking_description='',
                genres=[sample_genres[1]]  # Jazz
            ),
            Venue(
                name='Mixed Venue',
                city='Mixed City',
                state='MC',
                address='789 Mixed St',
                phone='555-123-4567',
                image_link='https://example.com/mixed-venue.jpg',
                facebook_link='https://facebook.com/mixedvenue',
                website_link='https://mixedvenue.com',
                seeking_talent=True,
                seeking_description='Looking for mixed talent',
                genres=[sample_genres[0], sample_genres[1]]  # Rock, Jazz
            ),
            Venue(
                name='Blues Venue',
                city='Blues City',
                state='BC',
                address='321 Blues St',
                phone='111-222-3333',
                image_link='https://example.com/blues-venue.jpg',
                facebook_link='https://facebook.com/bluesvenue',
                website_link='https://bluesvenue.com',
                seeking_talent=True,
                seeking_description='Looking for blues talent',
                genres=[sample_genres[2]]  # Blues
            ),
            Venue(
                name='Classical Venue',
                city='Classical City',
                state='CC',
                address='654 Classical St',
                phone='444-555-6666',
                image_link='https://example.com/classical-venue.jpg',
                facebook_link='https://facebook.com/classicalvenue',
                website_link='https://classicalvenue.com',
                seeking_talent=False,
                seeking_description='',
                genres=[sample_genres[3]]  # Classical
            )
        ]
        
        for venue in venues:
            db.session.add(venue)
        db.session.commit()
        
        return venues


@pytest.fixture
def sample_artists(app, sample_genres):
    """Create sample artists for testing."""
    with app.app_context():
        artists = [
            Artist(
                name='Rock Artist',
                city='Rock City',
                state='RC',
                phone='123-456-7890',
                image_link='https://example.com/rock-artist.jpg',
                facebook_link='https://facebook.com/rockartist',
                website_link='https://rockartist.com',
                seeking_venue=True,
                seeking_description='Looking for rock venues',
                genres=[sample_genres[0]]  # Rock
            ),
            Artist(
                name='Jazz Artist',
                city='Jazz City',
                state='JC',
                phone='987-654-3210',
                image_link='https://example.com/jazz-artist.jpg',
                facebook_link='https://facebook.com/jazzartist',
                website_link='https://jazzartist.com',
                seeking_venue=False,
                seeking_description='',
                genres=[sample_genres[1]]  # Jazz
            ),
            Artist(
                name='Mixed Artist',
                city='Mixed City',
                state='MC',
                phone='555-123-4567',
                image_link='https://example.com/mixed-artist.jpg',
                facebook_link='https://facebook.com/mixedartist',
                website_link='https://mixedartist.com',
                seeking_venue=True,
                seeking_description='Looking for mixed venues',
                genres=[sample_genres[0], sample_genres[1]]  # Rock, Jazz
            ),
            Artist(
                name='Blues Artist',
                city='Blues City',
                state='BC',
                phone='111-222-3333',
                image_link='https://example.com/blues-artist.jpg',
                facebook_link='https://facebook.com/bluesartist',
                website_link='https://bluesartist.com',
                seeking_venue=True,
                seeking_description='Looking for blues venues',
                genres=[sample_genres[2]]  # Blues
            ),
            Artist(
                name='Classical Artist',
                city='Classical City',
                state='CC',
                phone='444-555-6666',
                image_link='https://example.com/classical-artist.jpg',
                facebook_link='https://facebook.com/classicalartist',
                website_link='https://classicalartist.com',
                seeking_venue=False,
                seeking_description='',
                genres=[sample_genres[3]]  # Classical
            )
        ]
        
        for artist in artists:
            db.session.add(artist)
        db.session.commit()
        
        return artists


@pytest.fixture
def sample_shows(app, sample_venues, sample_artists):
    """Create sample shows for testing."""
    with app.app_context():
        shows = [
            Show(
                artist_id=sample_artists[0].id,  # Rock Artist
                venue_id=sample_venues[0].id,    # Rock Venue
                start_time=datetime.utcnow() + timedelta(days=1)
            ),
            Show(
                artist_id=sample_artists[1].id,  # Jazz Artist
                venue_id=sample_venues[1].id,    # Jazz Venue
                start_time=datetime.utcnow() + timedelta(days=7)
            ),
            Show(
                artist_id=sample_artists[2].id,  # Mixed Artist
                venue_id=sample_venues[2].id,    # Mixed Venue
                start_time=datetime.utcnow() + timedelta(days=14)
            ),
            Show(
                artist_id=sample_artists[3].id,  # Blues Artist
                venue_id=sample_venues[3].id,    # Blues Venue
                start_time=datetime.utcnow() + timedelta(days=21)
            ),
            Show(
                artist_id=sample_artists[4].id,  # Classical Artist
                venue_id=sample_venues[4].id,    # Classical Venue
                start_time=datetime.utcnow() + timedelta(days=28)
            ),
            # Past shows
            Show(
                artist_id=sample_artists[0].id,  # Rock Artist
                venue_id=sample_venues[1].id,    # Jazz Venue
                start_time=datetime.utcnow() - timedelta(days=30)
            ),
            Show(
                artist_id=sample_artists[1].id,  # Jazz Artist
                venue_id=sample_venues[2].id,    # Mixed Venue
                start_time=datetime.utcnow() - timedelta(days=60)
            ),
            Show(
                artist_id=sample_artists[2].id,  # Mixed Artist
                venue_id=sample_venues[3].id,    # Blues Venue
                start_time=datetime.utcnow() - timedelta(days=90)
            )
        ]
        
        for show in shows:
            db.session.add(show)
        db.session.commit()
        
        return shows


@pytest.fixture
def sample_data(app, sample_genres, sample_venues, sample_artists, sample_shows):
    """Create complete sample dataset for testing."""
    with app.app_context():
        return {
            'genres': sample_genres,
            'venues': sample_venues,
            'artists': sample_artists,
            'shows': sample_shows
        }


@pytest.fixture
def large_dataset(app):
    """Create large dataset for performance testing."""
    with app.app_context():
        # Create genres
        genres = []
        for i in range(20):
            genre = Genre(name=f'Genre {i}')
            db.session.add(genre)
            genres.append(genre)
        db.session.commit()
        
        # Create venues
        venues = []
        for i in range(50):
            venue = Venue(
                name=f'Performance Test Venue {i}',
                city=f'Performance Test City {i % 10}',  # 10 different cities
                state='PT',
                address=f'{i} Performance Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description=f'Looking for performance test talent {i}'
            )
            # Assign random genres
            venue.genres.extend(genres[i % 5:i % 5 + 2])  # 2 genres per venue
            db.session.add(venue)
            venues.append(venue)
        
        # Create artists
        artists = []
        for i in range(50):
            artist = Artist(
                name=f'Performance Test Artist {i}',
                city=f'Performance Test City {i % 10}',  # 10 different cities
                state='PT',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description=f'Looking for performance test venues {i}'
            )
            # Assign random genres
            artist.genres.extend(genres[i % 5:i % 5 + 2])  # 2 genres per artist
            db.session.add(artist)
            artists.append(artist)
        
        db.session.commit()
        
        # Create shows
        shows = []
        for i in range(100):
            show = Show(
                artist_id=artists[i % 50].id,
                venue_id=venues[i % 50].id,
                start_time=datetime.utcnow() + timedelta(days=i)
            )
            db.session.add(show)
            shows.append(show)
        
        db.session.commit()
        
        return {
            'genres': genres,
            'venues': venues,
            'artists': artists,
            'shows': shows
        }


@pytest.fixture
def invalid_data():
    """Provide invalid data for testing validation."""
    return {
        'invalid_phone': '1234567890',  # No dashes
        'invalid_state': 'INVALID',     # Invalid state code
        'invalid_genres': ['Invalid Genre'],  # Invalid genre
        'empty_name': '',              # Empty name
        'empty_city': '',              # Empty city
        'empty_genres': [],            # Empty genres list
        'invalid_url': 'not-a-url',    # Invalid URL
        'invalid_email': 'not-an-email',  # Invalid email
        'invalid_date': 'invalid-date',    # Invalid date
        'negative_id': -1,             # Negative ID
        'zero_id': 0,                  # Zero ID
        'large_id': 999999,            # Large ID
        'special_chars': '!@#$%^&*()', # Special characters
        'unicode_chars': '测试',        # Unicode characters
        'sql_injection': "'; DROP TABLE venues; --",  # SQL injection attempt
        'xss_attempt': '<script>alert("xss")</script>',  # XSS attempt
        'long_string': 'x' * 1000,    # Very long string
        'null_value': None,            # Null value
        'boolean_string': 'true',      # Boolean as string
        'number_string': '123',        # Number as string
        'array_string': '["item1", "item2"]',  # Array as string
        'object_string': '{"key": "value"}',   # Object as string
    }


@pytest.fixture
def edge_case_data():
    """Provide edge case data for testing."""
    return {
        'min_length_string': 'a',      # Minimum length string
        'max_length_string': 'x' * 255,  # Maximum length string
        'boundary_phone': '123-456-7890',  # Boundary phone
        'boundary_state': 'CA',         # Boundary state
        'boundary_genre': 'Rock',       # Boundary genre
        'boundary_url': 'https://example.com',  # Boundary URL
        'boundary_date': datetime.utcnow().isoformat(),  # Boundary date
        'boundary_id': 1,               # Boundary ID
        'boundary_boolean': True,       # Boundary boolean
        'boundary_number': 1,          # Boundary number
        'boundary_float': 1.0,          # Boundary float
        'boundary_list': ['item'],      # Boundary list
        'boundary_dict': {'key': 'value'},  # Boundary dict
        'whitespace_string': '   ',     # Whitespace only
        'tab_string': '\t',             # Tab character
        'newline_string': '\n',         # Newline character
        'carriage_return_string': '\r', # Carriage return character
        'mixed_whitespace': ' \t\n\r ', # Mixed whitespace
        'leading_whitespace': '  text', # Leading whitespace
        'trailing_whitespace': 'text  ', # Trailing whitespace
        'mixed_case': 'MiXeD cAsE',     # Mixed case
        'uppercase': 'UPPERCASE',       # Uppercase
        'lowercase': 'lowercase',       # Lowercase
        'camelCase': 'camelCase',       # Camel case
        'snake_case': 'snake_case',     # Snake case
        'kebab-case': 'kebab-case',     # Kebab case
        'PascalCase': 'PascalCase',     # Pascal case
    }


@pytest.fixture
def performance_data():
    """Provide performance test data."""
    return {
        'small_dataset': 10,    # Small dataset size
        'medium_dataset': 100,  # Medium dataset size
        'large_dataset': 1000,  # Large dataset size
        'xlarge_dataset': 10000, # Extra large dataset size
        'concurrent_requests': 10,  # Concurrent requests
        'timeout_seconds': 30,     # Timeout in seconds
        'memory_limit_mb': 100,    # Memory limit in MB
        'cpu_limit_percent': 80,   # CPU limit percentage
        'disk_space_mb': 1000,    # Disk space in MB
        'network_latency_ms': 100, # Network latency in milliseconds
        'response_time_ms': 1000,  # Response time in milliseconds
        'throughput_rps': 100,     # Throughput in requests per second
        'error_rate_percent': 5,   # Error rate percentage
        'availability_percent': 99.9,  # Availability percentage
    }


@pytest.fixture
def test_scenarios():
    """Provide test scenarios for different use cases."""
    return {
        'happy_path': {
            'description': 'Normal successful operation',
            'expected_result': 'success',
            'data': {'name': 'Test', 'city': 'Test City', 'state': 'TC'}
        },
        'error_path': {
            'description': 'Error condition',
            'expected_result': 'error',
            'data': {'name': '', 'city': '', 'state': ''}
        },
        'edge_case': {
            'description': 'Edge case scenario',
            'expected_result': 'edge_case',
            'data': {'name': 'a', 'city': 'a', 'state': 'CA'}
        },
        'boundary_case': {
            'description': 'Boundary condition',
            'expected_result': 'boundary',
            'data': {'name': 'x' * 255, 'city': 'x' * 120, 'state': 'CA'}
        },
        'performance_case': {
            'description': 'Performance scenario',
            'expected_result': 'performance',
            'data': {'name': 'Perf Test', 'city': 'Perf City', 'state': 'PC'}
        },
        'security_case': {
            'description': 'Security scenario',
            'expected_result': 'security',
            'data': {'name': '<script>alert("xss")</script>', 'city': 'Test City', 'state': 'TC'}
        },
        'concurrency_case': {
            'description': 'Concurrency scenario',
            'expected_result': 'concurrency',
            'data': {'name': 'Concurrent Test', 'city': 'Concurrent City', 'state': 'CC'}
        },
        'integration_case': {
            'description': 'Integration scenario',
            'expected_result': 'integration',
            'data': {'name': 'Integration Test', 'city': 'Integration City', 'state': 'IC'}
        }
    }

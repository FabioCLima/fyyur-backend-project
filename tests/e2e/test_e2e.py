"""
End-to-end tests for the Fyyur application.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre


class TestE2EVenueWorkflow:
    """End-to-end tests for venue workflow."""
    
    def test_complete_venue_lifecycle(self, client, app):
        """Test complete venue lifecycle from creation to deletion."""
        with app.app_context():
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Test venue creation
            response = client.post('/venues/create', data={
                'name': 'E2E Test Venue',
                'city': 'E2E Test City',
                'state': 'ET',
                'address': '123 E2E Test St',
                'phone': '123-456-7890',
                'image_link': 'https://example.com/venue.jpg',
                'facebook_link': 'https://facebook.com/e2etestvenue',
                'website_link': 'https://e2etestvenue.com',
                'seeking_talent': True,
                'seeking_description': 'Looking for E2E test talent',
                'genres': ['Rock', 'Jazz']
            })
            
            # Should redirect to venue show page
            assert response.status_code == 302
            assert '/venues/' in response.location
            
            # Get the venue ID from the redirect
            venue_id = int(response.location.split('/')[-1])
            
            # Test venue show page
            response = client.get(f'/venues/{venue_id}')
            assert response.status_code == 200
            assert b'E2E Test Venue' in response.data
            assert b'E2E Test City' in response.data
            assert b'ET' in response.data
            
            # Test venue edit form
            response = client.get(f'/venues/{venue_id}/edit')
            assert response.status_code == 200
            assert b'edit' in response.data.lower()
            
            # Test venue update
            response = client.post(f'/venues/{venue_id}/edit', data={
                'name': 'Updated E2E Test Venue',
                'phone': '987-654-3210',
                'seeking_description': 'Updated E2E test description'
            })
            
            # Should redirect to venue show page
            assert response.status_code == 302
            assert f'/venues/{venue_id}' in response.location
            
            # Verify update
            response = client.get(f'/venues/{venue_id}')
            assert response.status_code == 200
            assert b'Updated E2E Test Venue' in response.data
            assert b'987-654-3210' in response.data
            
            # Test venue search
            response = client.post('/venues/search', data={'search_term': 'E2E'})
            assert response.status_code == 200
            assert b'search' in response.data.lower()
            
            # Test venue API
            response = client.get('/venues/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['name'] == 'Updated E2E Test Venue'
            
            # Test venue API show
            response = client.get(f'/venues/api/{venue_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == 'Updated E2E Test Venue'
            assert data['city'] == 'E2E Test City'
            assert data['state'] == 'ET'
            
            # Test venue deletion
            response = client.post(f'/venues/{venue_id}/delete')
            assert response.status_code == 302
            assert '/venues/' in response.location
            
            # Verify venue is deleted
            response = client.get(f'/venues/{venue_id}')
            assert response.status_code == 302  # Should redirect to index


class TestE2EArtistWorkflow:
    """End-to-end tests for artist workflow."""
    
    def test_complete_artist_lifecycle(self, client, app):
        """Test complete artist lifecycle from creation to deletion."""
        with app.app_context():
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Test artist creation
            response = client.post('/artists/create', data={
                'name': 'E2E Test Artist',
                'city': 'E2E Test City',
                'state': 'ET',
                'phone': '123-456-7890',
                'image_link': 'https://example.com/artist.jpg',
                'facebook_link': 'https://facebook.com/e2etestartist',
                'website_link': 'https://e2etestartist.com',
                'seeking_venue': True,
                'seeking_description': 'Looking for E2E test venues',
                'genres': ['Rock', 'Jazz']
            })
            
            # Should redirect to artist show page
            assert response.status_code == 302
            assert '/artists/' in response.location
            
            # Get the artist ID from the redirect
            artist_id = int(response.location.split('/')[-1])
            
            # Test artist show page
            response = client.get(f'/artists/{artist_id}')
            assert response.status_code == 200
            assert b'E2E Test Artist' in response.data
            assert b'E2E Test City' in response.data
            assert b'ET' in response.data
            
            # Test artist edit form
            response = client.get(f'/artists/{artist_id}/edit')
            assert response.status_code == 200
            assert b'edit' in response.data.lower()
            
            # Test artist update
            response = client.post(f'/artists/{artist_id}/edit', data={
                'name': 'Updated E2E Test Artist',
                'phone': '987-654-3210',
                'seeking_description': 'Updated E2E test description'
            })
            
            # Should redirect to artist show page
            assert response.status_code == 302
            assert f'/artists/{artist_id}' in response.location
            
            # Verify update
            response = client.get(f'/artists/{artist_id}')
            assert response.status_code == 200
            assert b'Updated E2E Test Artist' in response.data
            assert b'987-654-3210' in response.data
            
            # Test artist search
            response = client.post('/artists/search', data={'search_term': 'E2E'})
            assert response.status_code == 200
            assert b'search' in response.data.lower()
            
            # Test artist API
            response = client.get('/artists/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['name'] == 'Updated E2E Test Artist'
            
            # Test artist API show
            response = client.get(f'/artists/api/{artist_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == 'Updated E2E Test Artist'
            assert data['city'] == 'E2E Test City'
            assert data['state'] == 'ET'
            
            # Test artist deletion
            response = client.post(f'/artists/{artist_id}/delete')
            assert response.status_code == 302
            assert '/artists/' in response.location
            
            # Verify artist is deleted
            response = client.get(f'/artists/{artist_id}')
            assert response.status_code == 302  # Should redirect to index


class TestE2EShowWorkflow:
    """End-to-end tests for show workflow."""
    
    def test_complete_show_lifecycle(self, client, app):
        """Test complete show lifecycle from creation to deletion."""
        with app.app_context():
            # Create genres first
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            # Create venue
            venue = Venue(
                name='E2E Test Venue',
                city='E2E Test City',
                state='ET',
                address='123 E2E Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for E2E test talent'
            )
            venue.genres.append(rock_genre)
            
            # Create artist
            artist = Artist(
                name='E2E Test Artist',
                city='E2E Test City',
                state='ET',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for E2E test venues'
            )
            artist.genres.append(rock_genre)
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.commit()
            
            # Test show creation form
            response = client.get('/shows/create')
            assert response.status_code == 200
            assert b'create' in response.data.lower()
            
            # Test show creation
            start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
            response = client.post('/shows/create', data={
                'artist_id': artist.id,
                'venue_id': venue.id,
                'start_time': start_time
            })
            
            # Should redirect to shows index
            assert response.status_code == 302
            assert '/shows/' in response.location
            
            # Get the show ID from the database
            show = Show.query.filter_by(artist_id=artist.id, venue_id=venue.id).first()
            assert show is not None
            show_id = show.id
            
            # Test show show page
            response = client.get(f'/shows/{show_id}')
            assert response.status_code == 200
            assert b'show' in response.data.lower()
            
            # Test show API
            response = client.get('/shows/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['artist_id'] == artist.id
            assert data[0]['venue_id'] == venue.id
            
            # Test show API show
            response = client.get(f'/shows/api/{show_id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['artist_id'] == artist.id
            assert data['venue_id'] == venue.id
            assert data['artist_name'] == 'E2E Test Artist'
            assert data['venue_name'] == 'E2E Test Venue'
            
            # Test upcoming shows API
            response = client.get('/shows/api/upcoming')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['id'] == show_id
            
            # Test past shows API
            response = client.get('/shows/api/past')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 0  # No past shows
            
            # Test show statistics API
            response = client.get('/shows/api/statistics')
            assert response.status_code == 200
            data = response.get_json()
            assert data['total_shows'] == 1
            assert data['upcoming_shows'] == 1
            assert data['past_shows'] == 0
            
            # Test show deletion
            response = client.post(f'/shows/{show_id}/delete')
            assert response.status_code == 302
            assert '/shows/' in response.location
            
            # Verify show is deleted
            response = client.get(f'/shows/{show_id}')
            assert response.status_code == 302  # Should redirect to index


class TestE2EHomepageWorkflow:
    """End-to-end tests for homepage workflow."""
    
    def test_homepage_with_data(self, client, app):
        """Test homepage with sample data."""
        with app.app_context():
            # Create genres
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            # Create venue
            venue = Venue(
                name='Homepage Test Venue',
                city='Homepage Test City',
                state='HT',
                address='123 Homepage Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for homepage test talent'
            )
            venue.genres.append(rock_genre)
            
            # Create artist
            artist = Artist(
                name='Homepage Test Artist',
                city='Homepage Test City',
                state='HT',
                phone='123-456-7890',
                seeking_venue=True,
                seeking_description='Looking for homepage test venues'
            )
            artist.genres.append(jazz_genre)
            
            # Create show
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.utcnow() + timedelta(days=1)
            )
            
            db.session.add(venue)
            db.session.add(artist)
            db.session.add(show)
            db.session.commit()
            
            # Test homepage
            response = client.get('/')
            assert response.status_code == 200
            assert b'Fyyur' in response.data
            
            # Test API stats
            response = client.get('/api/stats')
            assert response.status_code == 200
            data = response.get_json()
            assert data['venues'] == 1
            assert data['artists'] == 1
            assert data['shows'] == 1
            assert 'show_stats' in data
            assert data['show_stats']['total_shows'] == 1
            assert data['show_stats']['upcoming_shows'] == 1
            assert data['show_stats']['past_shows'] == 0


class TestE2EErrorHandling:
    """End-to-end tests for error handling."""
    
    def test_venue_not_found_error(self, client, app):
        """Test venue not found error handling."""
        with app.app_context():
            # Test non-existent venue
            response = client.get('/venues/999')
            assert response.status_code == 302  # Should redirect to index
            
            # Test non-existent venue API
            response = client.get('/venues/api/999')
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
    
    def test_artist_not_found_error(self, client, app):
        """Test artist not found error handling."""
        with app.app_context():
            # Test non-existent artist
            response = client.get('/artists/999')
            assert response.status_code == 302  # Should redirect to index
            
            # Test non-existent artist API
            response = client.get('/artists/api/999')
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
    
    def test_show_not_found_error(self, client, app):
        """Test show not found error handling."""
        with app.app_context():
            # Test non-existent show
            response = client.get('/shows/999')
            assert response.status_code == 302  # Should redirect to index
            
            # Test non-existent show API
            response = client.get('/shows/api/999')
            assert response.status_code == 404
            data = response.get_json()
            assert 'error' in data
    
    def test_validation_errors(self, client, app):
        """Test validation error handling."""
        with app.app_context():
            # Test venue creation with invalid data
            response = client.post('/venues/create', data={
                'name': '',  # Empty name
                'city': 'Test City',
                'state': 'TC',
                'address': '123 Test St',
                'genres': ['Rock']
            })
            assert response.status_code == 302  # Should redirect back to form
            
            # Test artist creation with invalid data
            response = client.post('/artists/create', data={
                'name': 'Test Artist',
                'city': '',  # Empty city
                'state': 'TC',
                'genres': ['Rock']
            })
            assert response.status_code == 302  # Should redirect back to form
            
            # Test show creation with invalid data
            response = client.post('/shows/create', data={
                'artist_id': '',  # Empty artist
                'venue_id': '1',
                'start_time': '2024-01-01T00:00:00'
            })
            assert response.status_code == 302  # Should redirect back to form
    
    def test_database_errors(self, client, app):
        """Test database error handling."""
        with app.app_context():
            # Test venue creation with duplicate name/city
            # First create a venue
            rock_genre = Genre(name='Rock')
            db.session.add(rock_genre)
            db.session.commit()
            
            venue = Venue(
                name='Duplicate Test Venue',
                city='Duplicate Test City',
                state='DT',
                address='123 Duplicate Test St',
                phone='123-456-7890',
                seeking_talent=True,
                seeking_description='Looking for duplicate test talent'
            )
            venue.genres.append(rock_genre)
            db.session.add(venue)
            db.session.commit()
            
            # Try to create another venue with same name/city
            response = client.post('/venues/create', data={
                'name': 'Duplicate Test Venue',
                'city': 'Duplicate Test City',
                'state': 'DT',
                'address': '456 Duplicate Test St',
                'phone': '987-654-3210',
                'seeking_talent': False,
                'seeking_description': '',
                'genres': ['Rock']
            })
            assert response.status_code == 302  # Should redirect back to form


class TestE2EPerformance:
    """End-to-end tests for performance."""
    
    def test_large_dataset_performance(self, client, app):
        """Test performance with large dataset."""
        with app.app_context():
            # Create genres
            genres = ['Rock', 'Jazz', 'Blues', 'Classical', 'Pop']
            for genre_name in genres:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            db.session.commit()
            
            # Create multiple venues
            for i in range(10):
                venue = Venue(
                    name=f'Performance Test Venue {i}',
                    city=f'Performance Test City {i}',
                    state='PT',
                    address=f'{i} Performance Test St',
                    phone='123-456-7890',
                    seeking_talent=True,
                    seeking_description=f'Looking for performance test talent {i}'
                )
                venue.genres.append(Genre.query.filter_by(name='Rock').first())
                db.session.add(venue)
            
            # Create multiple artists
            for i in range(10):
                artist = Artist(
                    name=f'Performance Test Artist {i}',
                    city=f'Performance Test City {i}',
                    state='PT',
                    phone='123-456-7890',
                    seeking_venue=True,
                    seeking_description=f'Looking for performance test venues {i}'
                )
                artist.genres.append(Genre.query.filter_by(name='Jazz').first())
                db.session.add(artist)
            
            db.session.commit()
            
            # Test venues index performance
            response = client.get('/venues/')
            assert response.status_code == 200
            
            # Test artists index performance
            response = client.get('/artists/')
            assert response.status_code == 200
            
            # Test shows index performance
            response = client.get('/shows/')
            assert response.status_code == 200
            
            # Test API performance
            response = client.get('/venues/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 10
            
            response = client.get('/artists/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 10
            
            response = client.get('/shows/api')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 0  # No shows created
            
            # Test search performance
            response = client.post('/venues/search', data={'search_term': 'Performance'})
            assert response.status_code == 200
            
            response = client.post('/artists/search', data={'search_term': 'Performance'})
            assert response.status_code == 200
            
            # Test statistics performance
            response = client.get('/api/stats')
            assert response.status_code == 200
            data = response.get_json()
            assert data['venues'] == 10
            assert data['artists'] == 10
            assert data['shows'] == 0

"""
Unit tests for controllers.
"""
import pytest
from datetime import datetime, timedelta
from app.models import db, Venue, Artist, Show, Genre
from app.exceptions import (
    VenueNotFoundException, DuplicateVenueException, DatabaseException,
    ArtistNotFoundException, DuplicateArtistException, ShowNotFoundException,
    ValidationException
)


class TestMainController:
    """Test cases for main controller."""
    
    def test_index(self, client, app, sample_venue, sample_artist, sample_show):
        """Test homepage."""
        with app.app_context():
            response = client.get('/')
            assert response.status_code == 200
            assert b'Fyyur' in response.data
    
    def test_api_stats(self, client, app, sample_venue, sample_artist, sample_show):
        """Test API stats endpoint."""
        with app.app_context():
            response = client.get('/api/stats')
            assert response.status_code == 200
            
            data = response.get_json()
            assert 'venues' in data
            assert 'artists' in data
            assert 'shows' in data
            assert 'show_stats' in data
            assert data['venues'] == 1
            assert data['artists'] == 1
            assert data['shows'] == 1


class TestVenueController:
    """Test cases for venue controller."""
    
    def test_index(self, client, app, sample_venue):
        """Test venue index page."""
        with app.app_context():
            response = client.get('/venues/')
            assert response.status_code == 200
            assert b'venues' in response.data.lower()
    
    def test_search_venues(self, client, app, sample_venue):
        """Test venue search."""
        with app.app_context():
            response = client.post('/venues/search', data={'search_term': 'Test'})
            assert response.status_code == 200
            assert b'search' in response.data.lower()
    
    def test_show_venue(self, client, app, sample_venue):
        """Test show venue page."""
        with app.app_context():
            response = client.get(f'/venues/{sample_venue.id}')
            assert response.status_code == 200
            assert b'Test Venue' in response.data
    
    def test_show_venue_not_found(self, client, app):
        """Test show venue not found."""
        with app.app_context():
            response = client.get('/venues/999')
            assert response.status_code == 302  # Redirect
    
    def test_create_venue_form(self, client, app):
        """Test create venue form."""
        with app.app_context():
            response = client.get('/venues/create')
            assert response.status_code == 200
            assert b'create' in response.data.lower()
    
    def test_create_venue_submit(self, client, app):
        """Test create venue submit."""
        with app.app_context():
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            response = client.post('/venues/create', data={
                'name': 'New Venue',
                'city': 'New City',
                'state': 'NC',
                'address': '123 New St',
                'phone': '123-456-7890',
                'seeking_talent': True,
                'seeking_description': 'Looking for talent',
                'genres': ['Rock', 'Jazz']
            })
            assert response.status_code == 302  # Redirect to show page
    
    def test_create_venue_validation_error(self, client, app):
        """Test create venue validation error."""
        with app.app_context():
            response = client.post('/venues/create', data={
                'name': '',  # Empty name
                'city': 'New City',
                'state': 'NC',
                'address': '123 New St',
                'genres': ['Rock']
            })
            assert response.status_code == 302  # Redirect back to form
    
    def test_edit_venue_form(self, client, app, sample_venue):
        """Test edit venue form."""
        with app.app_context():
            response = client.get(f'/venues/{sample_venue.id}/edit')
            assert response.status_code == 200
            assert b'edit' in response.data.lower()
    
    def test_edit_venue_submit(self, client, app, sample_venue):
        """Test edit venue submit."""
        with app.app_context():
            response = client.post(f'/venues/{sample_venue.id}/edit', data={
                'name': 'Updated Venue',
                'phone': '987-654-3210'
            })
            assert response.status_code == 302  # Redirect to show page
    
    def test_delete_venue(self, client, app, sample_venue):
        """Test delete venue."""
        with app.app_context():
            response = client.post(f'/venues/{sample_venue.id}/delete')
            assert response.status_code == 302  # Redirect to index
    
    def test_delete_venue_with_shows(self, client, app, sample_venue, sample_show):
        """Test delete venue with shows should fail."""
        with app.app_context():
            response = client.post(f'/venues/{sample_venue.id}/delete')
            assert response.status_code == 302  # Redirect to index
    
    def test_api_list_venues(self, client, app, sample_venue):
        """Test API list venues."""
        with app.app_context():
            response = client.get('/venues/api')
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['name'] == 'Test Venue'
    
    def test_api_show_venue(self, client, app, sample_venue):
        """Test API show venue."""
        with app.app_context():
            response = client.get(f'/venues/api/{sample_venue.id}')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data['name'] == 'Test Venue'
            assert data['city'] == 'Test City'
            assert data['state'] == 'TC'
    
    def test_api_show_venue_not_found(self, client, app):
        """Test API show venue not found."""
        with app.app_context():
            response = client.get('/venues/api/999')
            assert response.status_code == 404


class TestArtistController:
    """Test cases for artist controller."""
    
    def test_index(self, client, app, sample_artist):
        """Test artist index page."""
        with app.app_context():
            response = client.get('/artists/')
            assert response.status_code == 200
            assert b'artists' in response.data.lower()
    
    def test_search_artists(self, client, app, sample_artist):
        """Test artist search."""
        with app.app_context():
            response = client.post('/artists/search', data={'search_term': 'Test'})
            assert response.status_code == 200
            assert b'search' in response.data.lower()
    
    def test_show_artist(self, client, app, sample_artist):
        """Test show artist page."""
        with app.app_context():
            response = client.get(f'/artists/{sample_artist.id}')
            assert response.status_code == 200
            assert b'Test Artist' in response.data
    
    def test_show_artist_not_found(self, client, app):
        """Test show artist not found."""
        with app.app_context():
            response = client.get('/artists/999')
            assert response.status_code == 302  # Redirect
    
    def test_create_artist_form(self, client, app):
        """Test create artist form."""
        with app.app_context():
            response = client.get('/artists/create')
            assert response.status_code == 200
            assert b'create' in response.data.lower()
    
    def test_create_artist_submit(self, client, app):
        """Test create artist submit."""
        with app.app_context():
            # Create genres first
            rock_genre = Genre(name='Rock')
            jazz_genre = Genre(name='Jazz')
            db.session.add(rock_genre)
            db.session.add(jazz_genre)
            db.session.commit()
            
            response = client.post('/artists/create', data={
                'name': 'New Artist',
                'city': 'New City',
                'state': 'NC',
                'phone': '123-456-7890',
                'seeking_venue': True,
                'seeking_description': 'Looking for venues',
                'genres': ['Rock', 'Jazz']
            })
            assert response.status_code == 302  # Redirect to show page
    
    def test_create_artist_validation_error(self, client, app):
        """Test create artist validation error."""
        with app.app_context():
            response = client.post('/artists/create', data={
                'name': '',  # Empty name
                'city': 'New City',
                'state': 'NC',
                'genres': ['Rock']
            })
            assert response.status_code == 302  # Redirect back to form
    
    def test_edit_artist_form(self, client, app, sample_artist):
        """Test edit artist form."""
        with app.app_context():
            response = client.get(f'/artists/{sample_artist.id}/edit')
            assert response.status_code == 200
            assert b'edit' in response.data.lower()
    
    def test_edit_artist_submit(self, client, app, sample_artist):
        """Test edit artist submit."""
        with app.app_context():
            response = client.post(f'/artists/{sample_artist.id}/edit', data={
                'name': 'Updated Artist',
                'phone': '987-654-3210'
            })
            assert response.status_code == 302  # Redirect to show page
    
    def test_delete_artist(self, client, app, sample_artist):
        """Test delete artist."""
        with app.app_context():
            response = client.post(f'/artists/{sample_artist.id}/delete')
            assert response.status_code == 302  # Redirect to index
    
    def test_delete_artist_with_shows(self, client, app, sample_artist, sample_show):
        """Test delete artist with shows should fail."""
        with app.app_context():
            response = client.post(f'/artists/{sample_artist.id}/delete')
            assert response.status_code == 302  # Redirect to index
    
    def test_api_list_artists(self, client, app, sample_artist):
        """Test API list artists."""
        with app.app_context():
            response = client.get('/artists/api')
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['name'] == 'Test Artist'
    
    def test_api_show_artist(self, client, app, sample_artist):
        """Test API show artist."""
        with app.app_context():
            response = client.get(f'/artists/api/{sample_artist.id}')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data['name'] == 'Test Artist'
            assert data['city'] == 'Test City'
            assert data['state'] == 'TC'
    
    def test_api_show_artist_not_found(self, client, app):
        """Test API show artist not found."""
        with app.app_context():
            response = client.get('/artists/api/999')
            assert response.status_code == 404


class TestShowController:
    """Test cases for show controller."""
    
    def test_index(self, client, app, sample_show):
        """Test show index page."""
        with app.app_context():
            response = client.get('/shows/')
            assert response.status_code == 200
            assert b'shows' in response.data.lower()
    
    def test_create_show_form(self, client, app, sample_venue, sample_artist):
        """Test create show form."""
        with app.app_context():
            response = client.get('/shows/create')
            assert response.status_code == 200
            assert b'create' in response.data.lower()
    
    def test_create_show_submit(self, client, app, sample_venue, sample_artist):
        """Test create show submit."""
        with app.app_context():
            start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
            response = client.post('/shows/create', data={
                'artist_id': sample_artist.id,
                'venue_id': sample_venue.id,
                'start_time': start_time
            })
            assert response.status_code == 302  # Redirect to index
    
    def test_create_show_validation_error(self, client, app):
        """Test create show validation error."""
        with app.app_context():
            response = client.post('/shows/create', data={
                'artist_id': '',  # Empty artist
                'venue_id': '1',
                'start_time': '2024-01-01T00:00:00'
            })
            assert response.status_code == 302  # Redirect back to form
    
    def test_show_show(self, client, app, sample_show):
        """Test show show page."""
        with app.app_context():
            response = client.get(f'/shows/{sample_show.id}')
            assert response.status_code == 200
            assert b'show' in response.data.lower()
    
    def test_show_show_not_found(self, client, app):
        """Test show show not found."""
        with app.app_context():
            response = client.get('/shows/999')
            assert response.status_code == 302  # Redirect
    
    def test_delete_show(self, client, app, sample_show):
        """Test delete show."""
        with app.app_context():
            response = client.post(f'/shows/{sample_show.id}/delete')
            assert response.status_code == 302  # Redirect to index
    
    def test_api_list_shows(self, client, app, sample_show):
        """Test API list shows."""
        with app.app_context():
            response = client.get('/shows/api')
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['artist_id'] == sample_show.artist_id
            assert data[0]['venue_id'] == sample_show.venue_id
    
    def test_api_show_show(self, client, app, sample_show):
        """Test API show show."""
        with app.app_context():
            response = client.get(f'/shows/api/{sample_show.id}')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data['artist_id'] == sample_show.artist_id
            assert data['venue_id'] == sample_show.venue_id
    
    def test_api_show_show_not_found(self, client, app):
        """Test API show show not found."""
        with app.app_context():
            response = client.get('/shows/api/999')
            assert response.status_code == 404
    
    def test_api_upcoming_shows(self, client, app, sample_show):
        """Test API upcoming shows."""
        with app.app_context():
            response = client.get('/shows/api/upcoming')
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['id'] == sample_show.id
    
    def test_api_past_shows(self, client, app):
        """Test API past shows."""
        with app.app_context():
            # Create a past show
            past_show = Show(
                artist_id=1,
                venue_id=1,
                start_time=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(past_show)
            db.session.commit()
            
            response = client.get('/shows/api/past')
            assert response.status_code == 200
            
            data = response.get_json()
            assert len(data) == 1
            assert data[0]['id'] == past_show.id
    
    def test_api_statistics(self, client, app, sample_show):
        """Test API statistics."""
        with app.app_context():
            response = client.get('/shows/api/statistics')
            assert response.status_code == 200
            
            data = response.get_json()
            assert 'total_shows' in data
            assert 'upcoming_shows' in data
            assert 'past_shows' in data
            assert data['total_shows'] == 1
            assert data['upcoming_shows'] == 1
            assert data['past_shows'] == 0

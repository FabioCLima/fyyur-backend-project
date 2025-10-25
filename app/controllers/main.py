"""
Main controller for the Fyyur application.
"""
from flask import Blueprint, render_template, jsonify
from app.services import VenueService, ArtistService, ShowService
from app.exceptions import DatabaseException

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage with recent data."""
    try:
        venue_service = VenueService()
        artist_service = ArtistService()
        show_service = ShowService()
        
        # Get recent data for homepage
        recent_venues = venue_service.get_all(limit=10)
        recent_artists = artist_service.get_all(limit=10)
        recent_shows = show_service.get_recent_shows(days=30, limit=10)
        
        return render_template('pages/home.html', 
                            venues=recent_venues,
                            artists=recent_artists,
                            shows=recent_shows)
    except DatabaseException as e:
        return render_template('pages/home.html', 
                             venues=[],
                             artists=[],
                             shows=[],
                             error=str(e))

@main_bp.route('/api/stats')
def api_stats():
    """API endpoint for application statistics."""
    try:
        venue_service = VenueService()
        artist_service = ArtistService()
        show_service = ShowService()
        
        stats = {
            'venues': venue_service.count(),
            'artists': artist_service.count(),
            'shows': show_service.count(),
            'show_stats': show_service.get_show_statistics()
        }
        
        return jsonify(stats)
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

"""
Show controller for show CRUD operations.
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash  # pyright: ignore[reportMissingImports]
from app.services import ShowService, VenueService, ArtistService
from app.schemas import ShowCreate
from app.exceptions import ShowNotFoundException, DatabaseException, ValidationException

shows_bp = Blueprint('shows', __name__, url_prefix='/shows')

@shows_bp.route('/')
def index():
    """List all shows."""
    try:
        show_service = ShowService()
        shows = show_service.get_all_with_details()
        
        return render_template('pages/shows.html', shows=shows)
    except DatabaseException as e:
        flash(f"Error loading shows: {str(e)}", 'error')
        return render_template('pages/shows.html', shows=[])

@shows_bp.route('/create', methods=['GET'])
def create_form():
    """Show create show form."""
    try:
        venue_service = VenueService()
        artist_service = ArtistService()
        
        venues = venue_service.get_all()
        artists = artist_service.get_all()
        
        return render_template('forms/new_show.html', 
                             venues=venues,
                             artists=artists)
    except DatabaseException as e:
        flash(f"Error loading form: {str(e)}", 'error')
        return redirect(url_for('shows.index'))

@shows_bp.route('/create', methods=['POST'])
def create_submit():
    """Create show."""
    try:
        show_service = ShowService()
        
        # Get form data
        form_data = {
            'artist_id': request.form.get('artist_id', type=int),
            'venue_id': request.form.get('venue_id', type=int),
            'start_time': request.form.get('start_time')
        }
        
        # Validate required fields
        if not form_data['artist_id']:
            raise ValidationException("Artist is required")
        if not form_data['venue_id']:
            raise ValidationException("Venue is required")
        if not form_data['start_time']:
            raise ValidationException("Start time is required")
        
        # Parse start time
        from datetime import datetime
        try:
            form_data['start_time'] = datetime.fromisoformat(form_data['start_time'].replace('Z', '+00:00'))
        except ValueError:
            raise ValidationException("Invalid start time format")
        
        # Validate show time
        show_service.validate_show_time(form_data['start_time'])
        
        # Create show
        show_create = ShowCreate(**form_data)
        show = show_service.create_show(show_create)
        
        flash(f"Show was successfully created!", 'success')
        return redirect(url_for('shows.index'))
        
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect(url_for('shows.create_form'))
    except DatabaseException as e:
        flash(f"Error creating show: {str(e)}", 'error')
        return redirect(url_for('shows.create_form'))

@shows_bp.route('/<int:show_id>')
def show(show_id):
    """Show show details."""
    try:
        show_service = ShowService()
        show_response = show_service.get_show_response(show_id)
        
        if not show_response:
            flash(f"Show with ID {show_id} not found", 'error')
            return redirect(url_for('shows.index'))
        
        return render_template('pages/show_show.html', show=show_response)
    except ShowNotFoundException as e:
        flash(str(e), 'error')
        return redirect(url_for('shows.index'))
    except DatabaseException as e:
        flash(f"Error loading show: {str(e)}", 'error')
        return redirect(url_for('shows.index'))

@shows_bp.route('/<int:show_id>/delete', methods=['POST'])
def delete(show_id):
    """Delete show."""
    try:
        show_service = ShowService()
        show = show_service.get_by_id(show_id)
        
        if not show:
            flash(f"Show with ID {show_id} not found", 'error')
            return redirect(url_for('shows.index'))
        
        success = show_service.delete_show(show_id)
        if success:
            flash(f"Show was successfully deleted!", 'success')
        else:
            flash(f"Error deleting show", 'error')
            
        return redirect(url_for('shows.index'))
        
    except DatabaseException as e:
        flash(str(e), 'error')
        return redirect(url_for('shows.index'))

# API endpoints
@shows_bp.route('/api')
def api_list():
    """API endpoint to list all shows."""
    try:
        show_service = ShowService()
        shows = show_service.get_all()
        return jsonify([show.to_dict() for show in shows])
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@shows_bp.route('/api/<int:show_id>')
def api_show(show_id):
    """API endpoint to show show details."""
    try:
        show_service = ShowService()
        show_response = show_service.get_show_response(show_id)
        
        if not show_response:
            return jsonify({'error': f"Show with ID {show_id} not found"}), 404
        
        return jsonify(show_response.model_dump())
    except ShowNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@shows_bp.route('/api/upcoming')
def api_upcoming():
    """API endpoint for upcoming shows."""
    try:
        show_service = ShowService()
        shows = show_service.get_upcoming_shows()
        return jsonify([show.to_dict() for show in shows])
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@shows_bp.route('/api/past')
def api_past():
    """API endpoint for past shows."""
    try:
        show_service = ShowService()
        shows = show_service.get_past_shows()
        return jsonify([show.to_dict() for show in shows])
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@shows_bp.route('/api/statistics')
def api_statistics():
    """API endpoint for show statistics."""
    try:
        show_service = ShowService()
        stats = show_service.get_show_statistics()
        return jsonify(stats)
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

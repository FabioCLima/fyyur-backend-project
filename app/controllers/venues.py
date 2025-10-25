"""
Venue controller for venue CRUD operations.
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services import VenueService
from app.schemas import VenueCreate, VenueUpdate
from app.exceptions import VenueNotFoundException, DuplicateVenueException, DatabaseException, ValidationException

venues_bp = Blueprint('venues', __name__, url_prefix='/venues')

@venues_bp.route('/')
def index():
    """List all venues grouped by area."""
    try:
        venue_service = VenueService()
        areas = venue_service.get_areas()
        
        # Group venues by area
        venues_by_area = {}
        for area in areas:
            city_state = f"{area['city']}, {area['state']}"
            venues = venue_service.get_venues_by_area(area['city'], area['state'])
            venues_by_area[city_state] = venues
        
        return render_template('pages/venues.html', 
                             areas=areas,
                             venues_by_area=venues_by_area)
    except DatabaseException as e:
        flash(f"Error loading venues: {str(e)}", 'error')
        return render_template('pages/venues.html', areas=[], venues_by_area={})

@venues_bp.route('/search', methods=['POST'])
def search():
    """Search venues."""
    try:
        search_term = request.form.get('search_term', '').strip()
        venue_service = VenueService()
        
        if search_term:
            venues = venue_service.search_venues(search_term)
            results = {
                'count': len(venues),
                'data': [venue.to_dict() for venue in venues]
            }
        else:
            results = {'count': 0, 'data': []}
        
        return render_template('pages/search_venues.html', 
                             results=results,
                             search_term=search_term)
    except DatabaseException as e:
        flash(f"Error searching venues: {str(e)}", 'error')
        return render_template('pages/search_venues.html', 
                             results={'count': 0, 'data': []},
                             search_term='')

@venues_bp.route('/<int:venue_id>')
def show(venue_id):
    """Show venue details."""
    try:
        venue_service = VenueService()
        venue_response = venue_service.get_venue_response(venue_id)
        
        if not venue_response:
            flash(f"Venue with ID {venue_id} not found", 'error')
            return redirect(url_for('venues.index'))
        
        return render_template('pages/show_venue.html', venue=venue_response)
    except VenueNotFoundException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.index'))
    except DatabaseException as e:
        flash(f"Error loading venue: {str(e)}", 'error')
        return redirect(url_for('venues.index'))

@venues_bp.route('/create', methods=['GET'])
def create_form():
    """Show create venue form."""
    try:
        from app.services import GenreService
        genre_service = GenreService()
        genres = genre_service.get_all_genre_names()
        
        return render_template('forms/new_venue.html', genres=genres)
    except DatabaseException as e:
        flash(f"Error loading form: {str(e)}", 'error')
        return redirect(url_for('venues.index'))

@venues_bp.route('/create', methods=['POST'])
def create_submit():
    """Create venue."""
    try:
        venue_service = VenueService()
        
        # Get form data
        form_data = {
            'name': request.form.get('name', '').strip(),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', '').strip(),
            'address': request.form.get('address', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'image_link': request.form.get('image_link', '').strip(),
            'facebook_link': request.form.get('facebook_link', '').strip(),
            'website_link': request.form.get('website_link', '').strip(),
            'seeking_talent': bool(request.form.get('seeking_talent')),
            'seeking_description': request.form.get('seeking_description', '').strip(),
            'genres': request.form.getlist('genres')
        }
        
        # Validate required fields
        if not form_data['name']:
            raise ValidationException("Venue name is required")
        if not form_data['city']:
            raise ValidationException("City is required")
        if not form_data['state']:
            raise ValidationException("State is required")
        if not form_data['genres']:
            raise ValidationException("At least one genre is required")
        
        # Create venue
        venue_create = VenueCreate(**form_data)
        venue = venue_service.create_venue(venue_create)
        
        flash(f"Venue '{venue.name}' was successfully created!", 'success')
        return redirect(url_for('venues.show', venue_id=venue.id))
        
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.create_form'))
    except DuplicateVenueException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.create_form'))
    except DatabaseException as e:
        flash(f"Error creating venue: {str(e)}", 'error')
        return redirect(url_for('venues.create_form'))

@venues_bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_form(venue_id):
    """Show edit venue form."""
    try:
        venue_service = VenueService()
        venue = venue_service.get_by_id(venue_id)
        
        if not venue:
            flash(f"Venue with ID {venue_id} not found", 'error')
            return redirect(url_for('venues.index'))
        
        from app.services import GenreService
        genre_service = GenreService()
        genres = genre_service.get_all_genre_names()
        
        return render_template('forms/edit_venue.html', 
                             venue=venue,
                             genres=genres)
    except DatabaseException as e:
        flash(f"Error loading form: {str(e)}", 'error')
        return redirect(url_for('venues.index'))

@venues_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_submit(venue_id):
    """Update venue."""
    try:
        venue_service = VenueService()
        
        # Get form data
        form_data = {
            'name': request.form.get('name', '').strip(),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', '').strip(),
            'address': request.form.get('address', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'image_link': request.form.get('image_link', '').strip(),
            'facebook_link': request.form.get('facebook_link', '').strip(),
            'website_link': request.form.get('website_link', '').strip(),
            'seeking_talent': bool(request.form.get('seeking_talent')),
            'seeking_description': request.form.get('seeking_description', '').strip(),
            'genres': request.form.getlist('genres')
        }
        
        # Remove empty values
        form_data = {k: v for k, v in form_data.items() if v}
        
        # Update venue
        venue_update = VenueUpdate(**form_data)
        venue = venue_service.update_venue(venue_id, venue_update)
        
        if venue:
            flash(f"Venue '{venue.name}' was successfully updated!", 'success')
            return redirect(url_for('venues.show', venue_id=venue.id))
        else:
            flash(f"Venue with ID {venue_id} not found", 'error')
            return redirect(url_for('venues.index'))
            
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.edit_form', venue_id=venue_id))
    except DuplicateVenueException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.edit_form', venue_id=venue_id))
    except DatabaseException as e:
        flash(f"Error updating venue: {str(e)}", 'error')
        return redirect(url_for('venues.edit_form', venue_id=venue_id))

@venues_bp.route('/<int:venue_id>/delete', methods=['POST'])
def delete(venue_id):
    """Delete venue."""
    try:
        venue_service = VenueService()
        venue = venue_service.get_by_id(venue_id)
        
        if not venue:
            flash(f"Venue with ID {venue_id} not found", 'error')
            return redirect(url_for('venues.index'))
        
        success = venue_service.delete_venue(venue_id)
        if success:
            flash(f"Venue '{venue.name}' was successfully deleted!", 'success')
        else:
            flash(f"Error deleting venue", 'error')
            
        return redirect(url_for('venues.index'))
        
    except DatabaseException as e:
        flash(str(e), 'error')
        return redirect(url_for('venues.index'))

# API endpoints
@venues_bp.route('/api')
def api_list():
    """API endpoint to list all venues."""
    try:
        venue_service = VenueService()
        venues = venue_service.get_all()
        return jsonify([venue.to_dict() for venue in venues])
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@venues_bp.route('/api/<int:venue_id>')
def api_show(venue_id):
    """API endpoint to show venue details."""
    try:
        venue_service = VenueService()
        venue_response = venue_service.get_venue_response(venue_id)
        
        if not venue_response:
            return jsonify({'error': f"Venue with ID {venue_id} not found"}), 404
        
        return jsonify(venue_response.model_dump())
    except VenueNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

"""
Artist controller for artist CRUD operations.
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.services import ArtistService
from app.schemas import ArtistCreate, ArtistUpdate
from app.exceptions import ArtistNotFoundException, DuplicateArtistException, DatabaseException, ValidationException

artists_bp = Blueprint('artists', __name__, url_prefix='/artists')

@artists_bp.route('/')
def index():
    """List all artists."""
    try:
        artist_service = ArtistService()
        artists = artist_service.get_all()
        
        return render_template('pages/artists.html', artists=artists)
    except DatabaseException as e:
        flash(f"Error loading artists: {str(e)}", 'error')
        return render_template('pages/artists.html', artists=[])

@artists_bp.route('/search', methods=['POST'])
def search():
    """Search artists."""
    try:
        search_term = request.form.get('search_term', '').strip()
        artist_service = ArtistService()
        
        if search_term:
            artists = artist_service.search_artists(search_term)
            results = {
                'count': len(artists),
                'data': [artist.to_dict() for artist in artists]
            }
        else:
            results = {'count': 0, 'data': []}
        
        return render_template('pages/search_artists.html', 
                             results=results,
                             search_term=search_term)
    except DatabaseException as e:
        flash(f"Error searching artists: {str(e)}", 'error')
        return render_template('pages/search_artists.html', 
                             results={'count': 0, 'data': []},
                             search_term='')

@artists_bp.route('/<int:artist_id>')
def show(artist_id):
    """Show artist details."""
    try:
        artist_service = ArtistService()
        artist_response = artist_service.get_artist_response(artist_id)
        
        if not artist_response:
            flash(f"Artist with ID {artist_id} not found", 'error')
            return redirect(url_for('artists.index'))
        
        return render_template('pages/show_artist.html', artist=artist_response)
    except ArtistNotFoundException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.index'))
    except DatabaseException as e:
        flash(f"Error loading artist: {str(e)}", 'error')
        return redirect(url_for('artists.index'))

@artists_bp.route('/create', methods=['GET'])
def create_form():
    """Show create artist form."""
    try:
        from app.services import GenreService
        genre_service = GenreService()
        genres = genre_service.get_all_genre_names()
        
        return render_template('forms/new_artist.html', genres=genres)
    except DatabaseException as e:
        flash(f"Error loading form: {str(e)}", 'error')
        return redirect(url_for('artists.index'))

@artists_bp.route('/create', methods=['POST'])
def create_submit():
    """Create artist."""
    try:
        artist_service = ArtistService()
        
        # Get form data
        form_data = {
            'name': request.form.get('name', '').strip(),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'image_link': request.form.get('image_link', '').strip(),
            'facebook_link': request.form.get('facebook_link', '').strip(),
            'website_link': request.form.get('website_link', '').strip(),
            'seeking_venue': bool(request.form.get('seeking_venue')),
            'seeking_description': request.form.get('seeking_description', '').strip(),
            'genres': request.form.getlist('genres')
        }
        
        # Validate required fields
        if not form_data['name']:
            raise ValidationException("Artist name is required")
        if not form_data['city']:
            raise ValidationException("City is required")
        if not form_data['state']:
            raise ValidationException("State is required")
        if not form_data['genres']:
            raise ValidationException("At least one genre is required")
        
        # Create artist
        artist_create = ArtistCreate(**form_data)
        artist = artist_service.create_artist(artist_create)
        
        flash(f"Artist '{artist.name}' was successfully created!", 'success')
        return redirect(url_for('artists.show', artist_id=artist.id))
        
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.create_form'))
    except DuplicateArtistException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.create_form'))
    except DatabaseException as e:
        flash(f"Error creating artist: {str(e)}", 'error')
        return redirect(url_for('artists.create_form'))

@artists_bp.route('/<int:artist_id>/edit', methods=['GET'])
def edit_form(artist_id):
    """Show edit artist form."""
    try:
        artist_service = ArtistService()
        artist = artist_service.get_by_id(artist_id)
        
        if not artist:
            flash(f"Artist with ID {artist_id} not found", 'error')
            return redirect(url_for('artists.index'))
        
        from app.services import GenreService
        genre_service = GenreService()
        genres = genre_service.get_all_genre_names()
        
        return render_template('forms/edit_artist.html', 
                             artist=artist,
                             genres=genres)
    except DatabaseException as e:
        flash(f"Error loading form: {str(e)}", 'error')
        return redirect(url_for('artists.index'))

@artists_bp.route('/<int:artist_id>/edit', methods=['POST'])
def edit_submit(artist_id):
    """Update artist."""
    try:
        artist_service = ArtistService()
        
        # Get form data
        form_data = {
            'name': request.form.get('name', '').strip(),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'image_link': request.form.get('image_link', '').strip(),
            'facebook_link': request.form.get('facebook_link', '').strip(),
            'website_link': request.form.get('website_link', '').strip(),
            'seeking_venue': bool(request.form.get('seeking_venue')),
            'seeking_description': request.form.get('seeking_description', '').strip(),
            'genres': request.form.getlist('genres')
        }
        
        # Remove empty values
        form_data = {k: v for k, v in form_data.items() if v}
        
        # Update artist
        artist_update = ArtistUpdate(**form_data)
        artist = artist_service.update_artist(artist_id, artist_update)
        
        if artist:
            flash(f"Artist '{artist.name}' was successfully updated!", 'success')
            return redirect(url_for('artists.show', artist_id=artist.id))
        else:
            flash(f"Artist with ID {artist_id} not found", 'error')
            return redirect(url_for('artists.index'))
            
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.edit_form', artist_id=artist_id))
    except DuplicateArtistException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.edit_form', artist_id=artist_id))
    except DatabaseException as e:
        flash(f"Error updating artist: {str(e)}", 'error')
        return redirect(url_for('artists.edit_form', artist_id=artist_id))

@artists_bp.route('/<int:artist_id>/delete', methods=['POST'])
def delete(artist_id):
    """Delete artist."""
    try:
        artist_service = ArtistService()
        artist = artist_service.get_by_id(artist_id)
        
        if not artist:
            flash(f"Artist with ID {artist_id} not found", 'error')
            return redirect(url_for('artists.index'))
        
        success = artist_service.delete_artist(artist_id)
        if success:
            flash(f"Artist '{artist.name}' was successfully deleted!", 'success')
        else:
            flash(f"Error deleting artist", 'error')
            
        return redirect(url_for('artists.index'))
        
    except DatabaseException as e:
        flash(str(e), 'error')
        return redirect(url_for('artists.index'))

# API endpoints
@artists_bp.route('/api')
def api_list():
    """API endpoint to list all artists."""
    try:
        artist_service = ArtistService()
        artists = artist_service.get_all()
        return jsonify([artist.to_dict() for artist in artists])
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

@artists_bp.route('/api/<int:artist_id>')
def api_show(artist_id):
    """API endpoint to show artist details."""
    try:
        artist_service = ArtistService()
        artist_response = artist_service.get_artist_response(artist_id)
        
        if not artist_response:
            return jsonify({'error': f"Artist with ID {artist_id} not found"}), 404
        
        return jsonify(artist_response.model_dump())
    except ArtistNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except DatabaseException as e:
        return jsonify({'error': str(e)}), 500

"""
Professional seed script for Fyyur application.
"""
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, Venue, Artist, Show, Genre


def clear_data():
    """Clear all existing data."""
    print("Clearing existing data...")
    try:
        Show.query.delete()
        Artist.query.delete()
        Venue.query.delete()
        Genre.query.delete()
        db.session.commit()
        print("✓ Data cleared")
    except Exception as e:
        print(f"⚠️  No existing data to clear: {str(e)}")
        db.session.rollback()


def seed_genres():
    """Seed genres."""
    print("Seeding genres...")
    
    genres_data = [
        'Alternative', 'Blues', 'Classical', 'Country', 'Electronic',
        'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
        'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B',
        'Reggae', 'Rock n Roll', 'Soul', 'Other'
    ]
    
    genres = {}
    for genre_name in genres_data:
        genre = Genre(name=genre_name)
        db.session.add(genre)
        genres[genre_name] = genre
    
    db.session.commit()
    print(f"✓ Seeded {len(genres_data)} genres")
    return genres


def seed_venues(genres):
    """Seed venues."""
    print("Seeding venues...")
    
    venues_data = [
        {
            'name': 'The Musical Hop',
            'city': 'San Francisco',
            'state': 'CA',
            'address': '1015 Folsom Street',
            'phone': '123-123-1234',
            'image_link': 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
            'facebook_link': 'https://www.facebook.com/TheMusicalHop',
            'website_link': 'https://www.themusicalhop.com',
            'seeking_talent': True,
            'seeking_description': 'We are on the lookout for a local artist to play every two weeks. Please call us.',
            'genres': ['Jazz', 'Reggae', 'Classical', 'Folk']
        },
        {
            'name': 'The Dueling Pianos Bar',
            'city': 'New York',
            'state': 'NY',
            'address': '335 Delancey Street',
            'phone': '914-003-1132',
            'image_link': 'https://images.unsplash.com/photo-1497032205916-ac7590e094d0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
            'facebook_link': 'https://www.facebook.com/TheDuelingPianosBar',
            'website_link': 'https://www.theduelingpianos.com',
            'seeking_talent': False,
            'seeking_description': None,
            'genres': ['Classical', 'R&B', 'Hip-Hop']
        },
        {
            'name': 'Park Square Live Music & Coffee',
            'city': 'San Francisco',
            'state': 'CA',
            'address': '165 Augustine Street',
            'phone': '415-000-1234',
            'image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
            'facebook_link': 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
            'website_link': 'https://www.parksquarelivemusicandcoffee.com',
            'seeking_talent': False,
            'seeking_description': None,
            'genres': ['Rock n Roll', 'Jazz', 'Folk']
        }
    ]
    
    venues = []
    for venue_data in venues_data:
        venue_genres_list = [genres[g] for g in venue_data.pop('genres')]
        venue = Venue(**venue_data)
        db.session.add(venue)
        db.session.flush()  # Flush to get the venue ID
        venue.genres = venue_genres_list
        venues.append(venue)
    
    db.session.commit()
    print(f"✓ Seeded {len(venues)} venues")
    return venues


def seed_artists(genres):
    """Seed artists."""
    print("Seeding artists...")
    
    artists_data = [
        {
            'name': 'Guns N Petals',
            'city': 'San Francisco',
            'state': 'CA',
            'phone': '326-123-5000',
            'image_link': 'https://images.unsplash.com/photo-1549213783-8284d343d90c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            'facebook_link': 'https://www.facebook.com/GunsNPetals',
            'website_link': 'https://www.gunsnpetals.com',
            'seeking_venue': True,
            'seeking_description': 'Looking for shows to play in the San Francisco Bay Area!',
            'genres': ['Rock n Roll', 'Heavy Metal', 'Punk']
        },
        {
            'name': 'Matt Quevedo',
            'city': 'New York',
            'state': 'NY',
            'phone': '300-400-5000',
            'image_link': 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            'facebook_link': 'https://www.facebook.com/MattQuevedo',
            'website_link': 'https://www.mattquevedo.com',
            'seeking_venue': False,
            'seeking_description': None,
            'genres': ['Jazz', 'Blues', 'Folk']
        },
        {
            'name': 'The Wild Sax Band',
            'city': 'San Francisco',
            'state': 'CA',
            'phone': '432-325-5432',
            'image_link': 'https://images.unsplash.com/photo-1558036117-dfd343858ed9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            'facebook_link': 'https://www.facebook.com/TheWildSaxBand',
            'website_link': 'https://www.thewildsaxband.com',
            'seeking_venue': False,
            'seeking_description': None,
            'genres': ['Jazz', 'Classical', 'Pop']
        }
    ]
    
    artists = []
    for artist_data in artists_data:
        artist_genres_list = [genres[g] for g in artist_data.pop('genres')]
        artist = Artist(**artist_data)
        db.session.add(artist)
        db.session.flush()  # Flush to get the artist ID
        artist.genres = artist_genres_list
        artists.append(artist)
    
    db.session.commit()
    print(f"✓ Seeded {len(artists)} artists")
    return artists


def seed_shows(venues, artists):
    """Seed shows."""
    print("Seeding shows...")
    
    shows_data = [
        {
            'venue_name': 'The Musical Hop',
            'artist_name': 'Guns N Petals',
            'start_time': datetime.utcnow() + timedelta(days=7)
        },
        {
            'venue_name': 'The Dueling Pianos Bar',
            'artist_name': 'Matt Quevedo',
            'start_time': datetime.utcnow() + timedelta(days=14)
        },
        {
            'venue_name': 'Park Square Live Music & Coffee',
            'artist_name': 'The Wild Sax Band',
            'start_time': datetime.utcnow() + timedelta(days=21)
        },
        {
            'venue_name': 'The Musical Hop',
            'artist_name': 'Matt Quevedo',
            'start_time': datetime.utcnow() - timedelta(days=30)
        },
        {
            'venue_name': 'The Dueling Pianos Bar',
            'artist_name': 'Guns N Petals',
            'start_time': datetime.utcnow() - timedelta(days=60)
        }
    ]
    
    shows = []
    for show_data in shows_data:
        venue = next((v for v in venues if v.name == show_data['venue_name']), None)
        artist = next((a for a in artists if a.name == show_data['artist_name']), None)
        
        if venue and artist:
            show = Show(
                venue_id=venue.id,
                artist_id=artist.id,
                start_time=show_data['start_time']
            )
            db.session.add(show)
            shows.append(show)
    
    db.session.commit()
    print(f"✓ Seeded {len(shows)} shows")
    return shows


def main():
    """Main seed function."""
    print("🌱 Starting Fyyur database seed...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created")
            
            # Clear existing data
            clear_data()
            
            # Seed data
            genres = seed_genres()
            venues = seed_venues(genres)
            artists = seed_artists(genres)
            shows = seed_shows(venues, artists)
            
            print("\n🎉 Seed completed successfully!")
            print(f"📊 Summary:")
            print(f"   • {len(genres)} genres")
            print(f"   • {len(venues)} venues")
            print(f"   • {len(artists)} artists")
            print(f"   • {len(shows)} shows")
            
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise


if __name__ == '__main__':
    main()

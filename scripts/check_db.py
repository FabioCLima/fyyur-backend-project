"""
Check database connection and status.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, Venue, Artist, Show, Genre


def check_connection():
    """Check database connection."""
    print("🔍 Checking database connection...")
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Test connection
            db.session.execute('SELECT 1')
            print("✓ Database connection successful")
            
            # Check tables
            tables = db.inspect(db.engine).get_table_names()
            print(f"✓ Found {len(tables)} tables: {', '.join(tables)}")
            
            # Check data counts
            venue_count = Venue.query.count()
            artist_count = Artist.query.count()
            show_count = Show.query.count()
            genre_count = Genre.query.count()
            
            print(f"📊 Data counts:")
            print(f"   • Venues: {venue_count}")
            print(f"   • Artists: {artist_count}")
            print(f"   • Shows: {show_count}")
            print(f"   • Genres: {genre_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False


if __name__ == '__main__':
    check_connection()

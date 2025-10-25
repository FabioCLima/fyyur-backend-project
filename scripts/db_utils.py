"""
Database utilities for Fyyur application.
"""
import sys
import os
import click
from flask.cli import with_appcontext

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create database tables."""
    db.create_all()
    click.echo('✓ Database initialized')


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Reset database (WARNING: deletes all data)."""
    if click.confirm('This will delete all data. Continue?'):
        db.drop_all()
        db.create_all()
        click.echo('✓ Database reset')


@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Populate database with sample data."""
    from scripts.seed import main
    main()
    click.echo('✓ Database seeded')


def register_commands(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)
    app.cli.add_command(seed_db_command)


if __name__ == '__main__':
    app = create_app('development')
    register_commands(app)
    
    with app.app_context():
        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == 'init':
                init_db_command()
            elif command == 'reset':
                reset_db_command()
            elif command == 'seed':
                seed_db_command()
            else:
                print(f"Unknown command: {command}")
        else:
            print("Available commands: init, reset, seed")

"""
Fyyur Backend Application Package

Aplicação Flask profissional para agendamento de shows musicais.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate

from app.models import db
from app.utils.formatters import format_datetime


def create_app(config_name='development'):
    """
    Application factory pattern.

    Args:
        config_name: Configuration environment ('development', 'testing', 'production')

    Returns:
        Configured Flask application
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Load configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db, directory='migrations')
    moment = Moment(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register filters
    register_filters(app)
    
    # Setup logging
    setup_logging(app)
    
    return app


def register_blueprints(app):
    """Register application blueprints."""
    from app.controllers.main import main_bp
    from app.controllers.venues import venues_bp
    from app.controllers.artists import artists_bp
    from app.controllers.shows import shows_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(venues_bp)
    app.register_blueprint(artists_bp)
    app.register_blueprint(shows_bp)


def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500


def register_filters(app):
    """Register Jinja2 filters."""
    app.jinja_env.filters['datetime'] = format_datetime


def setup_logging(app):
    """Setup application logging."""
    if not app.debug and not app.testing:
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # File handler
        file_handler = RotatingFileHandler(
            'logs/fyyur.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Fyyur startup')


__all__ = ['create_app']

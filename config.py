"""
Configuration classes for different environments.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Session
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Flask-Migrate
    MIGRATION_DIR = os.path.join(os.path.dirname(__file__), 'migrations')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/fyyur.log'
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 10


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    
    # Database - SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(os.path.dirname(__file__), "fyyur.db")}'
    
    # Logging
    SQLALCHEMY_ECHO = True  # Log SQL queries in development


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    
    # Database - In-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Database - PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    
    # Logging
    LOG_LEVEL = 'WARNING'
    
    def __init__(self):
        super().__init__()
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable must be set in production")


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

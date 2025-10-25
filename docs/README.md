# 🎵 Fyyur - Musical Venue & Artist Booking Platform

> **Professional Backend Implementation**  
> A Flask-based web application for connecting musical artists with venues for live performances.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.20-red.svg)](https://sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.3.0-orange.svg)](https://pydantic.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Fyyur** is a comprehensive platform that connects musical artists with venues for live performances. Built with modern Python web development practices, it provides a robust backend system for managing venues, artists, and show bookings.

### Key Capabilities

- **Venue Management**: Complete CRUD operations for music venues
- **Artist Profiles**: Comprehensive artist profiles with genre management
- **Show Booking**: Schedule and manage live performances
- **Advanced Search**: Case-insensitive search with filtering capabilities
- **Data Validation**: Multi-layer validation using Pydantic and WTForms
- **Professional Architecture**: Clean separation of concerns with services and repositories

---

## ✨ Features

### Core Features
- ✅ **Venue CRUD**: Create, read, update, delete venues
- ✅ **Artist CRUD**: Complete artist profile management
- ✅ **Show Management**: Schedule and track performances
- ✅ **Genre System**: Normalized genre management
- ✅ **Search Functionality**: Advanced search with filters
- ✅ **Data Validation**: Robust validation at multiple layers
- ✅ **Database Migrations**: Version-controlled schema changes
- ✅ **Professional Logging**: Comprehensive logging system

### Advanced Features
- 🔄 **Application Factory Pattern**: Clean app initialization
- 🏗️ **Layered Architecture**: Services, repositories, controllers
- 📊 **Pydantic Schemas**: Type-safe data validation
- 🛡️ **Custom Exceptions**: Proper error handling
- 🧪 **Comprehensive Testing**: Unit and integration tests
- 📝 **Type Hints**: Full type annotation support
- 🔧 **Multiple Environments**: Development, testing, production configs

---

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────┐
│         Presentation Layer                  │
│  (Templates, Forms, HTTP Handlers)          │
│         Flask Blueprints                    │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Application Layer                   │
│    (Business Logic, Validators)             │
│       Service Classes                       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Data Access Layer                  │
│   (Repositories, Query Builders)           │
│       SQLAlchemy Models                     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Database Layer                     │
│         PostgreSQL/SQLite                  │
└─────────────────────────────────────────────┘
```

### Design Principles

- **Single Responsibility**: Each class has one clear purpose
- **Dependency Injection**: Services receive dependencies via constructor
- **Interface Segregation**: Small, focused interfaces
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It

---

## 🛠️ Tech Stack

### Backend Framework
- **Flask 2.3.3**: Web framework
- **SQLAlchemy 2.0.20**: ORM and database toolkit
- **Flask-Migrate**: Database migrations
- **Flask-WTF**: Form handling and CSRF protection
- **Flask-Moment**: Date/time formatting

### Data Validation
- **Pydantic 2.3.0**: Data validation and serialization
- **WTForms**: Web form handling

### Database
- **PostgreSQL**: Production database
- **SQLite**: Development and testing database

### Development Tools
- **UV**: Modern Python package manager
- **pytest**: Testing framework
- **Ruff**: Fast Python linter and formatter
- **pre-commit**: Git hooks for code quality

---

## 📁 Project Structure

```
fyyur-backend-project/
│
├── app/                              # Main application package
│   ├── __init__.py                   # Application factory
│   │
│   ├── models/                       # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py                   # Base model class
│   │   ├── venue.py                  # Venue model
│   │   ├── artist.py                 # Artist model
│   │   ├── show.py                   # Show model
│   │   └── genre.py                  # Genre model
│   │
│   ├── schemas/                      # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── common.py                 # Base schemas
│   │   ├── venue_schema.py           # Venue schemas
│   │   ├── artist_schema.py          # Artist schemas
│   │   └── show_schema.py            # Show schemas
│   │
│   ├── repositories/                 # Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py        # Generic repository
│   │   ├── venue_repository.py       # Venue-specific queries
│   │   ├── artist_repository.py      # Artist-specific queries
│   │   └── show_repository.py        # Show-specific queries
│   │
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── venue_service.py          # Venue business logic
│   │   ├── artist_service.py         # Artist business logic
│   │   └── show_service.py           # Show business logic
│   │
│   ├── controllers/                  # Flask blueprints
│   │   ├── __init__.py
│   │   ├── main.py                   # Homepage routes
│   │   ├── venues.py                 # Venue CRUD routes
│   │   ├── artists.py                # Artist CRUD routes
│   │   └── shows.py                  # Show CRUD routes
│   │
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py             # Custom validators
│   │   ├── formatters.py             # Data formatters
│   │   └── constants.py              # Application constants
│   │
│   └── exceptions/                   # Custom exceptions
│       ├── __init__.py
│       ├── base.py                   # Base exception
│       └── errors.py                 # Specific exceptions
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   ├── fixtures/                     # Test data fixtures
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   └── e2e/                         # End-to-end tests
│
├── scripts/                          # Utility scripts
│   ├── seed.py                       # Database seeding
│   ├── db_utils.py                   # Database utilities
│   └── check_db.py                   # Database health check
│
├── migrations/                       # Database migrations
├── static/                           # Static assets
├── templates/                        # Jinja2 templates
├── logs/                             # Application logs
│
├── app.py                            # Application entry point
├── config.py                         # Configuration classes
├── forms.py                          # WTForms (legacy compatibility)
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project configuration
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- UV package manager
- PostgreSQL (for production)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fyyur-backend-project
   ```

2. **Install UV (if not already installed)**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

4. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Seed the database**
   ```bash
   python scripts/seed.py
   ```

8. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=sqlite:///fyyur.db  # Development
# DATABASE_URL=postgresql://user:pass@localhost:5432/fyyur  # Production

# Security
SECRET_KEY=your-secret-key-here
WTF_CSRF_SECRET_KEY=csrf-secret-key

# Flask
FLASK_APP=app.py
FLASK_ENV=development

# Logging
LOG_LEVEL=INFO
```

### Configuration Classes

The application supports multiple environments:

- **Development**: SQLite database, debug mode enabled
- **Testing**: In-memory SQLite, CSRF disabled
- **Production**: PostgreSQL, security features enabled

---

## 📖 Usage

### Basic Operations

#### Venues
```python
# List all venues
GET /venues

# Search venues
POST /venues/search
{
    "search_term": "jazz"
}

# Get venue details
GET /venues/<id>

# Create venue
POST /venues/create

# Update venue
POST /venues/<id>/edit

# Delete venue
POST /venues/<id>/delete
```

#### Artists
```python
# List all artists
GET /artists

# Search artists
POST /artists/search

# Get artist details
GET /artists/<id>

# Create artist
POST /artists/create

# Update artist
POST /artists/<id>/edit
```

#### Shows
```python
# List all shows
GET /shows

# Create show
POST /shows/create

# Get show details
GET /shows/<id>
```

### Database Management

#### Migrations
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

#### Seeding
```bash
# Seed database with sample data
python scripts/seed.py

# Check database status
python scripts/check_db.py
```

---

## 📚 API Documentation

### Data Models

#### Venue
```python
{
    "id": 1,
    "name": "The Musical Hop",
    "city": "San Francisco",
    "state": "CA",
    "address": "1015 Folsom Street",
    "phone": "123-123-1234",
    "image_link": "https://example.com/image.jpg",
    "facebook_link": "https://facebook.com/venue",
    "website_link": "https://venue.com",
    "genres": ["Jazz", "Blues"],
    "seeking_talent": true,
    "seeking_description": "Looking for local artists",
    "upcoming_shows_count": 2,
    "past_shows_count": 5,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Artist
```python
{
    "id": 1,
    "name": "Guns N Petals",
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "image_link": "https://example.com/artist.jpg",
    "facebook_link": "https://facebook.com/artist",
    "website_link": "https://artist.com",
    "genres": ["Rock n Roll", "Heavy Metal"],
    "seeking_venue": true,
    "seeking_description": "Looking for shows",
    "upcoming_shows_count": 3,
    "past_shows_count": 8,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Show
```python
{
    "id": 1,
    "artist_id": 1,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://example.com/artist.jpg",
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "venue_image_link": "https://example.com/venue.jpg",
    "start_time": "2024-02-01T20:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Validation Rules

#### Venue Validation
- `name`: Required, 1-255 characters
- `city`: Required, 1-120 characters
- `state`: Required, exactly 2 uppercase letters
- `phone`: Optional, format XXX-XXX-XXXX
- `genres`: Required, at least 1 genre from allowed list

#### Artist Validation
- `name`: Required, 1-255 characters
- `city`: Required, 1-120 characters
- `state`: Required, exactly 2 uppercase letters
- `phone`: Optional, format XXX-XXX-XXXX
- `genres`: Required, at least 1 genre from allowed list

#### Show Validation
- `artist_id`: Required, must exist
- `venue_id`: Required, must exist
- `start_time`: Required, must be in the future

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run with verbose output
pytest -v
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows

### Test Coverage

The project aims for >80% test coverage across all modules.

---

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run flask db upgrade
   heroku run python scripts/seed.py
   ```

### Docker Deployment

```bash
# Build image
docker build -t fyyur-app .

# Run container
docker run -p 5000:5000 fyyur-app
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation as needed
- Use meaningful commit messages
- Ensure all tests pass before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- SQLAlchemy team for the powerful ORM
- Pydantic team for data validation
- UV team for the modern package manager
- All contributors and the open-source community

---

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the code examples

---

**Built with ❤️ using Flask, SQLAlchemy, and Pydantic**
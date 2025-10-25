"""
Unit tests for exceptions.
"""
import pytest
from app.exceptions import (
    FyyurException, VenueNotFoundException, DuplicateVenueException,
    ArtistNotFoundException, DuplicateArtistException, ShowNotFoundException,
    ValidationException, DatabaseException, ConflictException
)


class TestFyyurException:
    """Test cases for FyyurException."""
    
    def test_fyyur_exception_default(self):
        """Test FyyurException with default status code."""
        message = "Test error message"
        exception = FyyurException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 400
    
    def test_fyyur_exception_custom_status_code(self):
        """Test FyyurException with custom status code."""
        message = "Test error message"
        status_code = 404
        exception = FyyurException(message, status_code)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == status_code
    
    def test_fyyur_exception_inheritance(self):
        """Test FyyurException inheritance."""
        message = "Test error message"
        exception = FyyurException(message)
        
        assert isinstance(exception, Exception)
        assert isinstance(exception, FyyurException)


class TestVenueExceptions:
    """Test cases for venue exceptions."""
    
    def test_venue_not_found_exception(self):
        """Test VenueNotFoundException."""
        message = "Venue not found"
        exception = VenueNotFoundException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 404
        assert isinstance(exception, FyyurException)
    
    def test_duplicate_venue_exception(self):
        """Test DuplicateVenueException."""
        message = "Venue already exists"
        exception = DuplicateVenueException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 409
        assert isinstance(exception, FyyurException)


class TestArtistExceptions:
    """Test cases for artist exceptions."""
    
    def test_artist_not_found_exception(self):
        """Test ArtistNotFoundException."""
        message = "Artist not found"
        exception = ArtistNotFoundException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 404
        assert isinstance(exception, FyyurException)
    
    def test_duplicate_artist_exception(self):
        """Test DuplicateArtistException."""
        message = "Artist already exists"
        exception = DuplicateArtistException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 409
        assert isinstance(exception, FyyurException)


class TestShowExceptions:
    """Test cases for show exceptions."""
    
    def test_show_not_found_exception(self):
        """Test ShowNotFoundException."""
        message = "Show not found"
        exception = ShowNotFoundException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 404
        assert isinstance(exception, FyyurException)


class TestValidationExceptions:
    """Test cases for validation exceptions."""
    
    def test_validation_exception(self):
        """Test ValidationException."""
        message = "Validation error"
        exception = ValidationException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 422
        assert isinstance(exception, FyyurException)


class TestDatabaseExceptions:
    """Test cases for database exceptions."""
    
    def test_database_exception(self):
        """Test DatabaseException."""
        message = "Database error"
        exception = DatabaseException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 500
        assert isinstance(exception, FyyurException)


class TestConflictExceptions:
    """Test cases for conflict exceptions."""
    
    def test_conflict_exception(self):
        """Test ConflictException."""
        message = "Resource conflict"
        exception = ConflictException(message)
        
        assert str(exception) == message
        assert exception.message == message
        assert exception.status_code == 409
        assert isinstance(exception, FyyurException)


class TestExceptionUsage:
    """Test cases for exception usage patterns."""
    
    def test_exception_raising(self):
        """Test raising exceptions."""
        with pytest.raises(VenueNotFoundException) as exc_info:
            raise VenueNotFoundException("Venue with ID 1 not found")
        
        assert exc_info.value.message == "Venue with ID 1 not found"
        assert exc_info.value.status_code == 404
    
    def test_exception_catching(self):
        """Test catching exceptions."""
        try:
            raise DuplicateVenueException("Venue 'Test Venue' already exists")
        except DuplicateVenueException as e:
            assert e.message == "Venue 'Test Venue' already exists"
            assert e.status_code == 409
        except Exception:
            pytest.fail("Should have caught DuplicateVenueException")
    
    def test_exception_inheritance_chain(self):
        """Test exception inheritance chain."""
        # All custom exceptions should inherit from FyyurException
        exceptions = [
            VenueNotFoundException("test"),
            DuplicateVenueException("test"),
            ArtistNotFoundException("test"),
            DuplicateArtistException("test"),
            ShowNotFoundException("test"),
            ValidationException("test"),
            DatabaseException("test"),
            ConflictException("test")
        ]
        
        for exception in exceptions:
            assert isinstance(exception, FyyurException)
            assert isinstance(exception, Exception)
    
    def test_exception_status_codes(self):
        """Test exception status codes."""
        status_codes = {
            VenueNotFoundException: 404,
            DuplicateVenueException: 409,
            ArtistNotFoundException: 404,
            DuplicateArtistException: 409,
            ShowNotFoundException: 404,
            ValidationException: 422,
            DatabaseException: 500,
            ConflictException: 409
        }
        
        for exception_class, expected_status in status_codes.items():
            exception = exception_class("test message")
            assert exception.status_code == expected_status
    
    def test_exception_message_preservation(self):
        """Test exception message preservation."""
        messages = [
            "Venue with ID 1 not found",
            "Artist 'Test Artist' already exists in Test City",
            "Show with ID 5 not found",
            "Invalid input data",
            "Database connection failed",
            "Cannot delete venue with existing shows"
        ]
        
        exception_classes = [
            VenueNotFoundException,
            DuplicateArtistException,
            ShowNotFoundException,
            ValidationException,
            DatabaseException,
            ConflictException
        ]
        
        for message, exception_class in zip(messages, exception_classes):
            exception = exception_class(message)
            assert exception.message == message
            assert str(exception) == message
    
    def test_exception_equality(self):
        """Test exception equality."""
        # Same exception type with same message should be equal
        exc1 = VenueNotFoundException("Test message")
        exc2 = VenueNotFoundException("Test message")
        
        # Note: Exception equality is based on type and message
        assert type(exc1) == type(exc2)
        assert exc1.message == exc2.message
        assert exc1.status_code == exc2.status_code
        
        # Different messages should not be equal
        exc3 = VenueNotFoundException("Different message")
        assert exc1.message != exc3.message
    
    def test_exception_string_representation(self):
        """Test exception string representation."""
        message = "Test error message"
        exception = VenueNotFoundException(message)
        
        # String representation should be the message
        assert str(exception) == message
        assert repr(exception) == f"VenueNotFoundException('{message}')"
    
    def test_exception_context_usage(self):
        """Test exception usage in context."""
        def find_venue(venue_id):
            if venue_id == 0:
                raise VenueNotFoundException(f"Venue with ID {venue_id} not found")
            return {"id": venue_id, "name": "Test Venue"}
        
        def find_artist(artist_id):
            if artist_id == 0:
                raise ArtistNotFoundException(f"Artist with ID {artist_id} not found")
            return {"id": artist_id, "name": "Test Artist"}
        
        # Test successful case
        venue = find_venue(1)
        assert venue["id"] == 1
        assert venue["name"] == "Test Venue"
        
        # Test exception case
        with pytest.raises(VenueNotFoundException):
            find_venue(0)
        
        # Test different exception type
        with pytest.raises(ArtistNotFoundException):
            find_artist(0)
    
    def test_exception_chaining(self):
        """Test exception chaining."""
        try:
            try:
                raise DatabaseException("Database connection failed")
            except DatabaseException as e:
                raise VenueNotFoundException("Could not find venue due to database error") from e
        except VenueNotFoundException as e:
            assert e.message == "Could not find venue due to database error"
            assert e.status_code == 404
            assert isinstance(e.__cause__, DatabaseException)
            assert e.__cause__.message == "Database connection failed"

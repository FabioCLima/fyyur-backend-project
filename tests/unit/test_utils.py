"""
Unit tests for utilities.
"""
import pytest
from datetime import datetime, timedelta
from app.utils import (
    validate_phone, validate_state_code, validate_genres,
    format_datetime, format_phone, format_address,
    VALID_GENRES, VALID_STATES, DEFAULT_PAGE_SIZE
)


class TestValidators:
    """Test cases for validators."""
    
    def test_validate_phone_valid(self):
        """Test valid phone numbers."""
        valid_phones = ['123-456-7890', '555-123-4567', '999-888-7777']
        for phone in valid_phones:
            result = validate_phone(phone)
            assert result == phone
    
    def test_validate_phone_invalid(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            '1234567890',      # No dashes
            '123-456-789',     # Too short
            '123-456-78901',   # Too long
            'abc-def-ghij',    # Non-numeric
            '123-456-789a',    # Mixed
            '',                # Empty
            '123-456-789-0'    # Extra dash
        ]
        for phone in invalid_phones:
            with pytest.raises(ValueError, match="Phone must be in format XXX-XXX-XXXX"):
                validate_phone(phone)
    
    def test_validate_state_code_valid(self):
        """Test valid state codes."""
        valid_states = ['CA', 'NY', 'TX', 'FL', 'WA', 'OR']
        for state in valid_states:
            result = validate_state_code(state)
            assert result == state.upper()
    
    def test_validate_state_code_invalid(self):
        """Test invalid state codes."""
        invalid_states = ['INVALID', 'C', 'CALIFORNIA', 'ca', 'Ca']
        for state in invalid_states:
            with pytest.raises(ValueError, match="Invalid state code"):
                validate_state_code(state)
    
    def test_validate_state_code_case_insensitive(self):
        """Test state code case insensitivity."""
        result = validate_state_code('ca')
        assert result == 'CA'
        
        result = validate_state_code('Ca')
        assert result == 'CA'
        
        result = validate_state_code('cA')
        assert result == 'CA'
    
    def test_validate_genres_valid(self):
        """Test valid genres."""
        valid_genre_lists = [
            ['Rock'],
            ['Rock', 'Jazz'],
            ['Rock', 'Jazz', 'Blues'],
            ['Classical', 'Pop', 'Electronic']
        ]
        for genres in valid_genre_lists:
            result = validate_genres(genres)
            assert result == genres
    
    def test_validate_genres_invalid(self):
        """Test invalid genres."""
        invalid_genre_lists = [
            [],  # Empty list
            ['Invalid Genre'],
            ['Rock', 'Invalid Genre'],
            ['Rock', 'Jazz', 'Invalid Genre', 'Blues']
        ]
        for genres in invalid_genre_lists:
            with pytest.raises(ValueError):
                validate_genres(genres)
    
    def test_validate_genres_empty_list(self):
        """Test empty genres list."""
        with pytest.raises(ValueError, match="At least one genre is required"):
            validate_genres([])
    
    def test_validate_genres_mixed_valid_invalid(self):
        """Test genres list with both valid and invalid genres."""
        with pytest.raises(ValueError, match="Invalid genres"):
            validate_genres(['Rock', 'Invalid Genre', 'Jazz'])


class TestFormatters:
    """Test cases for formatters."""
    
    def test_format_datetime_full(self):
        """Test full datetime format."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result = format_datetime(dt, 'full')
        assert 'Monday' in result
        assert 'January' in result
        assert '15' in result
        assert '2024' in result
        assert '2:30PM' in result
    
    def test_format_datetime_medium(self):
        """Test medium datetime format."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result = format_datetime(dt, 'medium')
        assert 'Mon' in result
        assert 'Jan' in result
        assert '15' in result
        assert '2024' in result
        assert '2:30PM' in result
    
    def test_format_datetime_short(self):
        """Test short datetime format."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result = format_datetime(dt, 'short')
        assert '01/15/2024' in result
        assert '2:30PM' in result
    
    def test_format_datetime_string_input(self):
        """Test datetime format with string input."""
        dt_string = '2024-01-15T14:30:00'
        result = format_datetime(dt_string, 'medium')
        assert 'Jan' in result
        assert '15' in result
        assert '2024' in result
    
    def test_format_datetime_invalid_format(self):
        """Test datetime format with invalid format."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result = format_datetime(dt, 'invalid')
        # Should default to short format
        assert '01/15/2024' in result
    
    def test_format_phone_valid(self):
        """Test phone formatting."""
        valid_phones = [
            '1234567890',
            '555-123-4567',
            '(555) 123-4567',
            '555.123.4567',
            '555 123 4567'
        ]
        for phone in valid_phones:
            result = format_phone(phone)
            assert result == '555-123-4567' or result == '123-456-7890'
    
    def test_format_phone_invalid(self):
        """Test phone formatting with invalid input."""
        invalid_phones = [
            '123456789',      # Too short
            '12345678901',    # Too long
            'abc-def-ghij',   # Non-numeric
            '',               # Empty
            None              # None
        ]
        for phone in invalid_phones:
            result = format_phone(phone)
            assert result == phone or result == ""
    
    def test_format_phone_empty(self):
        """Test phone formatting with empty input."""
        result = format_phone('')
        assert result == ''
        
        result = format_phone(None)
        assert result == ''
    
    def test_format_address(self):
        """Test address formatting."""
        result = format_address('San Francisco', 'CA')
        assert result == 'San Francisco, CA'
        
        result = format_address('New York', 'NY')
        assert result == 'New York, NY'
        
        result = format_address('Los Angeles', 'CA')
        assert result == 'Los Angeles, CA'


class TestConstants:
    """Test cases for constants."""
    
    def test_valid_genres(self):
        """Test valid genres constant."""
        assert isinstance(VALID_GENRES, set)
        assert len(VALID_GENRES) > 0
        assert 'Rock' in VALID_GENRES
        assert 'Jazz' in VALID_GENRES
        assert 'Blues' in VALID_GENRES
        assert 'Classical' in VALID_GENRES
        assert 'Pop' in VALID_GENRES
        assert 'Electronic' in VALID_GENRES
        assert 'Folk' in VALID_GENRES
        assert 'Funk' in VALID_GENRES
        assert 'Hip-Hop' in VALID_GENRES
        assert 'Heavy Metal' in VALID_GENRES
        assert 'Instrumental' in VALID_GENRES
        assert 'Musical Theatre' in VALID_GENRES
        assert 'Punk' in VALID_GENRES
        assert 'R&B' in VALID_GENRES
        assert 'Reggae' in VALID_GENRES
        assert 'Rock n Roll' in VALID_GENRES
        assert 'Soul' in VALID_GENRES
        assert 'Other' in VALID_GENRES
    
    def test_valid_states(self):
        """Test valid states constant."""
        assert isinstance(VALID_STATES, set)
        assert len(VALID_STATES) == 51  # 50 states + DC
        assert 'CA' in VALID_STATES
        assert 'NY' in VALID_STATES
        assert 'TX' in VALID_STATES
        assert 'FL' in VALID_STATES
        assert 'WA' in VALID_STATES
        assert 'OR' in VALID_STATES
        assert 'DC' in VALID_STATES
        assert 'AL' in VALID_STATES
        assert 'AK' in VALID_STATES
        assert 'AZ' in VALID_STATES
        assert 'AR' in VALID_STATES
        assert 'CO' in VALID_STATES
        assert 'CT' in VALID_STATES
        assert 'DE' in VALID_STATES
        assert 'GA' in VALID_STATES
        assert 'HI' in VALID_STATES
        assert 'ID' in VALID_STATES
        assert 'IL' in VALID_STATES
        assert 'IN' in VALID_STATES
        assert 'IA' in VALID_STATES
        assert 'KS' in VALID_STATES
        assert 'KY' in VALID_STATES
        assert 'LA' in VALID_STATES
        assert 'ME' in VALID_STATES
        assert 'MD' in VALID_STATES
        assert 'MA' in VALID_STATES
        assert 'MI' in VALID_STATES
        assert 'MN' in VALID_STATES
        assert 'MS' in VALID_STATES
        assert 'MO' in VALID_STATES
        assert 'MT' in VALID_STATES
        assert 'NE' in VALID_STATES
        assert 'NV' in VALID_STATES
        assert 'NH' in VALID_STATES
        assert 'NJ' in VALID_STATES
        assert 'NM' in VALID_STATES
        assert 'NC' in VALID_STATES
        assert 'ND' in VALID_STATES
        assert 'OH' in VALID_STATES
        assert 'OK' in VALID_STATES
        assert 'PA' in VALID_STATES
        assert 'RI' in VALID_STATES
        assert 'SC' in VALID_STATES
        assert 'SD' in VALID_STATES
        assert 'TN' in VALID_STATES
        assert 'UT' in VALID_STATES
        assert 'VT' in VALID_STATES
        assert 'VA' in VALID_STATES
        assert 'WV' in VALID_STATES
        assert 'WI' in VALID_STATES
        assert 'WY' in VALID_STATES
    
    def test_default_page_size(self):
        """Test default page size constant."""
        assert isinstance(DEFAULT_PAGE_SIZE, int)
        assert DEFAULT_PAGE_SIZE == 10
        assert DEFAULT_PAGE_SIZE > 0


class TestUtilityIntegration:
    """Test cases for utility integration."""
    
    def test_phone_validation_and_formatting(self):
        """Test phone validation and formatting together."""
        # Valid phone that needs formatting
        phone = '1234567890'
        formatted = format_phone(phone)
        assert formatted == '123-456-7890'
        
        # Validate the formatted phone
        validated = validate_phone(formatted)
        assert validated == '123-456-7890'
    
    def test_state_validation_and_formatting(self):
        """Test state validation and formatting together."""
        # Valid state that needs formatting
        state = 'ca'
        validated = validate_state_code(state)
        assert validated == 'CA'
        
        # Format address with validated state
        address = format_address('San Francisco', validated)
        assert address == 'San Francisco, CA'
    
    def test_genre_validation_with_constants(self):
        """Test genre validation with constants."""
        # Test that all valid genres pass validation
        for genre in VALID_GENRES:
            result = validate_genres([genre])
            assert result == [genre]
        
        # Test that invalid genres fail validation
        invalid_genres = ['Invalid Genre', 'Rock and Roll', 'Jazz Fusion']
        for genre in invalid_genres:
            with pytest.raises(ValueError):
                validate_genres([genre])
    
    def test_datetime_formatting_with_different_inputs(self):
        """Test datetime formatting with different input types."""
        # Test with datetime object
        dt = datetime(2024, 1, 15, 14, 30, 0)
        result1 = format_datetime(dt, 'medium')
        
        # Test with ISO string
        dt_string = '2024-01-15T14:30:00'
        result2 = format_datetime(dt_string, 'medium')
        
        # Results should be similar (allowing for minor differences)
        assert 'Jan' in result1
        assert 'Jan' in result2
        assert '15' in result1
        assert '15' in result2
        assert '2024' in result1
        assert '2024' in result2

"""
Utility functions for the Fyyur application.
"""
import re
from typing import Optional


def validate_phone(phone: str) -> str:
    """Validate phone number format."""
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    if not re.match(pattern, phone):
        raise ValueError('Phone must be in format XXX-XXX-XXXX')
    return phone


def validate_state_code(state: str) -> str:
    """Validate US state code."""
    VALID_STATES = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
        'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
        'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
        'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
        'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    state = state.upper()
    if state not in VALID_STATES:
        raise ValueError(f'Invalid state code: {state}')
    return state


def validate_genres(genres: list) -> list:
    """Validate list of genres."""
    VALID_GENRES = {
        'Alternative', 'Blues', 'Classical', 'Country', 'Electronic',
        'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
        'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B',
        'Reggae', 'Rock n Roll', 'Soul', 'Other'
    }
    
    if not genres:
        raise ValueError('At least one genre is required')
    
    invalid = set(genres) - VALID_GENRES
    if invalid:
        raise ValueError(f'Invalid genres: {", ".join(invalid)}')
    
    return genres

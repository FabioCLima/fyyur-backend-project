"""
Constants for the Fyyur application.
"""
from typing import Set

# Valid music genres
VALID_GENRES: Set[str] = {
    'Alternative', 'Blues', 'Classical', 'Country', 'Electronic',
    'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
    'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B',
    'Reggae', 'Rock n Roll', 'Soul', 'Other'
}

# Valid US state codes
VALID_STATES: Set[str] = {
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
    'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
    'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
}

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Search defaults
MAX_SEARCH_RESULTS = 50

# File upload limits
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

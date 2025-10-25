"""
Formatters for the Fyyur application.
"""
import re
from babel import dates
import dateutil.parser
from datetime import datetime


def format_datetime(value, format='medium'):
    """
    Format datetime for display in templates.
    
    Args:
        value: datetime object or string
        format: format type ('full', 'medium', 'short')
        
    Returns:
        Formatted datetime string
    """
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
        
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    else:  # short
        format = "MM/dd/yyyy h:mma"
        
    return dates.format_datetime(date, format, locale='en')


def format_phone(phone: str) -> str:
    """Format phone number for display."""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format as XXX-XXX-XXXX
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    return phone


def format_address(city: str, state: str) -> str:
    """Format city and state for display."""
    return f"{city}, {state}"

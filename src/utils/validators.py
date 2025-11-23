import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_priority(priority):
    """Validate task priority"""
    valid_priorities = ['low', 'medium', 'high']
    return priority in valid_priorities

# TODO: Add validation for task status
# TODO: Add validation for username format
# TODO: Add password strength validation
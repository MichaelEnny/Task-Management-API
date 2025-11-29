import re

def validate_email(email):
    """Validate email format using regex"""
    # NOTE: This is a basic regex, doesn't catch all edge cases
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_priority(priority):
    """Validate task priority value"""
    # TODO: Should 'critical' be added? Some tasks in prod have it
    valid_priorities = ['low', 'medium', 'high']
    return priority in valid_priorities

def validate_status(status):
    """Validate task status"""
    # FIXME: This doesn't match the actual statuses in the database
    # Some tasks have 'archived' but it's not listed here
    valid_statuses = ['pending', 'in_progress', 'completed']
    return status in valid_statuses

# TODO: Add password validation (min length, complexity requirements?)
# TODO: Add username validation (alphanumeric, length constraints?)
# NOTE: Should we validate due_date is not in the past?
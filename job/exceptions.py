"""
Exceptions relating to Job creation and acess
"""


class JobCreationError(Exception):
    """on failure to create a new job"""
    pass


class JobNotFoundError(Exception):
    """Invalid job id"""
    pass


class JobAccessError(Exception):
    """No access to job"""
    pass
"""
Exceptions relating to Job creation and acess
"""


class JobCreationError(Exception):
    """on failure to create a new impression_job"""
    pass


class JobNotFoundError(Exception):
    """Invalid impression_job id"""
    pass


class JobAccessError(Exception):
    """No access to impression_job"""
    pass

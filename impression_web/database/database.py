"""
Base class for database tooling
"""
import abc


class Database(abc.ABC):
    """
    Platform agnostic database tooling
    """
    @abc.abstractmethod
    def user_job_ids(self, username) -> [int]:
        """Return list of id belonging to the username"""
        pass

    @abc.abstractmethod
    def user_jobs(self, username) -> [dict]:
        """Return list of Job objects belonging to the username"""
        pass

"""
Google firestore access
"""
from typing import Iterable

from google.cloud import firestore

from impression_web.database.database import Database
from impression_web.job.gcp_job import GCPJob


class GCPDatabase(Database):
    """
    Database management for Google Cloud Platform NoSQL document database
    Overloads user_job_ids and user_jobs methods from parent

    """
    J_COLLECTION_PATH = u'jobs'

    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = firestore.Client()

        return self._db

    def _jobs_collection(self) -> firestore.CollectionReference:
        """Return reference to jobs root in database"""
        return self.db.collection(GCPDatabase.J_COLLECTION_PATH)

    def _job_reference(self, job_id: str) -> firestore.DocumentReference:
        """Get reference to specific job_id"""
        return self._jobs_collection().document(job_id)

    def user_job_ids(self, username: str) -> Iterable[int]:
        """Return iterator of job id associated with username"""
        jobs = self._user_jobs(username)
        return GCPDatabase._ids_from_jobs(jobs)

    def user_jobs(self, username: str) -> Iterable[GCPJob]:
        """return iterator of Job instances associated with username"""
        jobs = self._user_jobs(username)
        return (GCPJob.from_dict(j.to_dict()) for j in jobs)

    def _user_jobs(self, username) -> Iterable[firestore.DocumentSnapshot]:
        """Helper: Query jobs associated with the username"""
        return self._jobs_collection().where(u'user', u'==', username).get()

    @staticmethod
    def _ids_from_jobs(
            jobs: Iterable[firestore.DocumentSnapshot]) -> Iterable[int]:
        """Helper: Exact job_ids from iterable of Job DocumentSnapshots"""
        return map(lambda x: x.to_dict()['job_id'], jobs)

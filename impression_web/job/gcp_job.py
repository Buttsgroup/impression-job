"""
IMPRESSION Job for GCP
"""
from google.cloud import firestore
from google.cloud.firestore import DocumentReference

from impression_web.job.exceptions import \
    JobCreationError, JobNotFoundError, JobAccessError
from impression_web.job.job import Job, JobStatus


class GCPJob(Job):
    """
    Impression Job for the google cloud platform (GCP)
    Representation of a job in the GCP database
    Allow update/deletion of own record in database

    Overloads delete_in_db, update_in_db, from_dict, from_id from parent Job

    Raises JobCreationError on invalid File dictionary
    Raises JobAccessError: init from db : permission denied
    Raises JobNotFoundError: init from db: no such impression_web id
    """

    def __init__(self,
                 user: str = None,
                 file: dict = None,
                 model: str = None,
                 job_id: str = None):
        super().__init__(user, file, model, job_id)

    @property
    def db(self):
        if self._db is None:
            self._db = firestore.Client()
        return self._db

    @staticmethod
    def from_dict(src: dict):
        job = GCPJob()
        for k, v in src.items():
            try:
                if 'time' in k:
                    setattr(job, k, Job._datetimefromstr(v))

                elif k == 'status':
                    setattr(job, k, JobStatus(v))
                else:
                    setattr(job, k, v)
            except AttributeError:
                pass

        return job

    @staticmethod
    def from_id(job_id: str, user: str,
                admin_access=None, db: firestore.Client = None):
        """
        Look up a job_id in the database
        Return the constructed Job object IF user matches Job.user
        Admin access allows non-matching user to query
        """
        if db is None:
            db = firestore.Client()

        job_ref = db.collection(u'jobs').document(job_id).get()

        if job_ref.exists:
            job = GCPJob.from_dict(job_ref.to_dict())
            if job.user == user or admin_access:
                return job
            else:
                raise JobAccessError(f"{user} does not own {job_id}")
        else:
            raise JobNotFoundError(f'{job_id} does not exist')

    def update_in_db(self, job_id=None) -> str:
        jid = self.job_id if job_id is None else job_id

        if (self.user is None and
                self.file is None and
                self.model is None):
            raise JobCreationError(
                f"""Cannot add empty impression_web to database:
                {self.user}, {self.file}, {self.model}""")

        # Passing None to document() generates a impression_web-id
        ref: DocumentReference = self.db.collection(u'jobs').document(jid)

        write_res: firestore.types.WriteResult = ref.set(self.to_dict())

        if write_res:
            self.job_id = ref.id

        return self.job_id

    def delete_in_db(self) -> bool:
        if self.job_id is not None:
            ref: DocumentReference = self.db.collection(
                u'jobs').document(self.job_id)

            ref.delete()
            return not ref.get().exists

        else:
            return False

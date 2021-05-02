"""
IMPRESSION Job: manage impression_job instances within firestore
JobAccessError, JobCreationError, JobNotFoundError
JobStatus enum
"""
import enum

from google.cloud import firestore
from google.cloud.firestore import DocumentReference

from impression_job.exceptions import JobCreationError, JobNotFoundError, \
    JobAccessError
from impression_job.firestore import ref_job
from impression_job.job import Job


class GCPJob(Job):
    """
    Impression Job for the google cloud platform (gcp)
    Raises JobCreationError on invalid File dictionary
    Raises JobAccessError: init from db : permission denied
    Raises JobNotFoundError: init from db: no such impression_job id
    """
    platform = 'gcp'

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

    def to_dict(self):
        return {u'job_id': self.job_id,
                u'user': self.user,
                u'status': self.status.value,
                u'input_name': self.input_name,
                u'upload_name': self._upload_name,
                u'output_name': self._output_name,
                u'model': self.model,
                u'submission_time': self.submission_time,
                u'start_time': self.start_time,
                u'completion_time': self.completion_time,
                u'info': self._info,
                u'err': self._err,
                u'output_file_url': self._output_file_url
                }

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
    def from_id(job_id: str, user: str):
        """
        Look up a job_id in the database
        Return the constructed Job object IF user matches Job.user
        """
        db = firestore.Client()

        job_ref = ref_job(db, job_id).get()
        if job_ref.exists:
            job = GCPJob.from_dict(job_ref.to_dict())
            if job.user == user:
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
                f"""Cannot add empty impression_job to database:
                {self.user}, {self.file}, {self.model}""")

        # Passing None to document() generates a impression_job-id
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


class JobStatus(enum.IntEnum):
    """
    Enumeration for Job states
    """
    NONE = 0
    SUBMITTED = 1
    QUEUED = 2
    STARTED = 3
    FINISHED = 4
    ERROR = 5

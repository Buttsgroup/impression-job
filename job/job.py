"""
IMPRESSION Job: manage job instances within firestore
JobAccessError, JobCreationError, JobNotFoundError
JobStatus enum
"""
from datetime import datetime
import enum

from google.cloud import firestore
from google.cloud.firestore import DocumentReference

from job.exceptions import JobCreationError, JobNotFoundError, JobAccessError
from job.firestore import ref_job


class Job:
    """
    Job object for IMPRESSION
    Raises JobCreationError on invalid File dictionary
    Raises JobAccessError: init from db : permission denied
    Raises JobNotFoundError: init from db: no such job id
    """
    _datetime_format = '%y-%m-%d::%H:%M'

    def __init__(self,
                 user: str = None,
                 file: dict = None,
                 model: str = None,
                 job_id: str = None):
        """
        Creating a new job via file upload
        """
        self.user = user
        self.file = file
        self.model = model
        self.job_id = job_id

        self._submission_time: datetime = None
        self._start_time: datetime = None
        self._completion_time: datetime = None

        self.status = JobStatus.NONE
        self._info = ""
        self._err = ""

        self._output_file_url = None

        self._db = None
        self._bucket = None

        try:
            self.input_name = file['input_name']
            self._upload_name = file['upload_name']
            self._output_name = None
        except KeyError as e:
            raise JobCreationError("Invalid file dictionary") from e
        except TypeError:
            self.input_name = None
            self._upload_name = None
            self._output_name = None

    @property
    def submission_time(self):
        try:
            return self._strfromdatetime(self._submission_time)
        except AttributeError:
            return None

    @property
    def start_time(self):
        try:
            return self._strfromdatetime(self._start_time)
        except AttributeError:
            return None

    @property
    def completion_time(self):
        try:
            return self._strfromdatetime(
                self._completion_time)
        except AttributeError:
            return None

    @property
    def output_file_url(self):
        return self._output_file_url

    @output_file_url.setter
    def output_file_url(self, value):
        self._output_file_url = value

    @property
    def upload_name(self):
        return self._upload_name

    @upload_name.setter
    def upload_name(self, value):
        self._upload_name = value

    @property
    def output_name(self):
        return self._upload_name

    @output_name.setter
    def output_name(self, value):
        self._output_name = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def err(self):
        return self._err

    @err.setter
    def err(self, value):
        self._err = value

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
        job = Job(user=None)
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
    def from_id(job_id: str, user: str, db: firestore.Client = None):
        """
        Look up a job_id in the database
        Return the constructed Job object IF user matches Job.user
        """
        if db is None:
            db = firestore.Client()

        job_ref = ref_job(db, job_id).get()
        if job_ref.exists:
            job = Job.from_dict(job_ref.to_dict())
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
                f"""Cannot add empty job to database:
                {self.user}, {self.file}, {self.model}""")

        # Passing None to document() generates a job-id
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

    @staticmethod
    def _datetimefromstr(string: str) -> datetime:
        try:
            return datetime.strptime(string, Job._datetime_format)
        except TypeError:
            return None

    @staticmethod
    def _strfromdatetime(dt: datetime) -> datetime:
        try:
            return dt.strftime(Job._datetime_format)
        except TypeError:
            return None


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

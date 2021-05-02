"""
Testing for Job object and method
"""
import unittest
import warnings

from impression_job.job_factory import ImpressionJobFactory
from impression_job.gc_job import Job
from impression_job.exceptions import JobCreationError, JobNotFoundError, \
    JobAccessError

from google.cloud import firestore


class TestGCPJob(unittest.TestCase):
    def setUp(self) -> None:
        """Create Initial Job"""
        warnings.simplefilter('ignore', ResourceWarning)
        self.job_factory = ImpressionJobFactory(platform='gcp')
        self.platform = 'gcp'

        self.test_job = self.job_factory.job(
            'test-user',
            {
                'input_name': 'test-input.sdf',
                'upload_name': 'test-upload.sdf'},
            model='fchl')

        self.test_dict = {'job_id': None, 'user': 'test-user', 'status': 0,
                          'input_name': 'test-input.sdf',
                          'upload_name': 'test-upload.sdf',
                          'output_name': None, 'model': 'fchl',
                          'submission_time': None,
                          'start_time': None, 'completion_time': None,
                          'info': '',
                          'err': '', 'output_file_url': None}

        # Upload to database
        self.test_job.update_in_db('test-impression_job')

    def test_db(self):
        self.assertTrue(isinstance(self.test_job.db, firestore.Client))

    def test_db_jobs_ref(self):
        docs = self.test_job.db.collection('jobs').list_documents(page_size=1)
        self.assertTrue(docs, 'jobs collection exists')

    def test_empty_to_dict(self):
        self.assertDictEqual(
            self.job_factory.job().to_dict(),
            {'job_id': None, 'user': None, 'status': 0, 'input_name': None,
             'upload_name': None, 'output_name': None, 'model': None,
             'submission_time': None, 'start_time': None,
             'completion_time': None, 'info': '', 'err': '',
             'output_file_url': None}
        )

    def test_invalid_file_dict(self):
        with self.assertRaises(JobCreationError):
            self.job_factory.job().update_in_db()

    def test_from_dict(self):
        self.assertDictEqual(
            self.job_factory.from_dict(self.test_dict).to_dict(),
            self.test_dict)

    def test_update(self):
        job_id = self.test_job.update_in_db('test-impression_job')

        self.assertEqual(self.test_job.job_id, 'test-impression_job')
        self.assertEqual(job_id, 'test-impression_job')

    def test_from_id(self):
        new_job = self.job_factory.from_id('test-impression_job', 'test-user')

        self.assertDictEqual(new_job.to_dict(), self.test_dict)

    def test_from_invalid_id(self):
        with self.assertRaises(JobNotFoundError):
            self.job_factory.from_id('invalid-id', 'user')

    def test_non_matching_user(self):
        with self.assertRaises(JobAccessError):
            self.job_factory.from_id('test-impression_job',
                                     'incorrect-user')

    def test_delete(self):
        job_to_delete = self.job_factory.from_dict(self.test_dict)
        job_to_delete.update_in_db('impression_job-to-delete')

        self.assertTrue(job_to_delete.delete_in_db())

    def test_output_url_unfinished(self):
        self.assertIs(self.test_job.output_file_url, None)

    def tearDown(self) -> None:
        self.test_job.db.document('jobs/test-impression_job').delete()

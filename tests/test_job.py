"""
Testing for Job object and method
"""
import unittest
import warnings

from impression_job.job.job_factory import ImpressionJobFactory
from impression_job.job.exceptions import JobCreationError, JobNotFoundError, \
    JobAccessError

from google.cloud import firestore


class TestGCPJob(unittest.TestCase):
    test_dict = None
    job_factory = None
    test_job = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.job_factory = ImpressionJobFactory(platform='gcp')
        cls.platform = 'gcp'

        cls.test_job = cls.job_factory.job(
            'test-user',
            {
                'input_name': 'test-input.sdf',
                'upload_name': 'test-upload.sdf'},
            model='fchl')

        cls.test_dict = {'job_id': None, 'user': 'test-user', 'status': 0,
                         'input_name': 'test-input.sdf',
                         'upload_name': 'test-upload.sdf',
                         'output_name': None, 'model': 'fchl',
                         'submission_time': None,
                         'start_time': None, 'completion_time': None,
                         'info': '',
                         'err': '', 'output_file_url': None}

        # Upload to database
        cls.test_job.update_in_db('test-impression_job')

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    def test_db(self):
        self.assertTrue(isinstance(TestGCPJob.test_job.db, firestore.Client))

    def test_db_jobs_ref(self):
        docs = self.test_job.db.collection('jobs').list_documents(page_size=1)
        self.assertTrue(docs, 'jobs collection exists')

    def test_empty_to_dict(self):
        self.assertDictEqual(
            TestGCPJob.job_factory.job().to_dict(),
            {'job_id': None, 'user': None, 'status': 0, 'input_name': None,
             'upload_name': None, 'output_name': None, 'model': None,
             'submission_time': None, 'start_time': None,
             'completion_time': None, 'info': '', 'err': '',
             'output_file_url': None}
        )

    def test_invalid_file_dict(self):
        with self.assertRaises(JobCreationError):
            TestGCPJob.job_factory.job().update_in_db()

    def test_from_dict(self):
        self.assertDictEqual(
            TestGCPJob.job_factory.from_dict(TestGCPJob.test_dict).to_dict(),
            TestGCPJob.test_dict)

    def test_update(self):
        job_id = TestGCPJob.test_job.update_in_db('test-impression_job')

        self.assertEqual(TestGCPJob.test_job.job_id, 'test-impression_job')
        self.assertEqual(job_id, 'test-impression_job')

    def test_from_id(self):
        new_job = TestGCPJob.job_factory.from_id('test-impression_job',
                                                 'test-user')

        self.assertDictEqual(new_job.to_dict(), TestGCPJob.test_dict)

    def test_from_invalid_id(self):
        with self.assertRaises(JobNotFoundError):
            TestGCPJob.job_factory.from_id('invalid-id', 'user')

    def test_non_matching_user(self):
        with self.assertRaises(JobAccessError):
            TestGCPJob.job_factory.from_id('test-impression_job',
                                           'incorrect-user')

    def test_delete(self):
        job_to_delete = TestGCPJob.job_factory.from_dict(TestGCPJob.test_dict)
        job_to_delete.update_in_db('impression_job-to-delete')

        self.assertTrue(job_to_delete.delete_in_db())

    def test_output_url_unfinished(self):
        self.assertIs(TestGCPJob.test_job.output_file_url, None)

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_job.db.document('jobs/test-impression_job').delete()

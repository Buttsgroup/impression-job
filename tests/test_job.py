"""
Testing for Job object and method
"""
import unittest
import warnings

from job import Job, JobCreationError, JobNotFoundError, JobAccessError

from google.cloud import firestore, storage


class TestJob(unittest.TestCase):
    def setUp(self) -> None:
        """Create Initial Job"""
        warnings.simplefilter("ignore", ResourceWarning)

        self.test_job = Job('test-user',
                            {'input_name': 'test-input.sdf',
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
        self.test_job.update_in_db('test-job')

    def test_db(self):
        self.assertTrue(isinstance(self.test_job.db, firestore.Client))

    def test_db_jobs_ref(self):
        docs = self.test_job.db.collection('jobs').list_documents(page_size=1)
        self.assertTrue(docs, 'jobs collection exists')

    def test_empty_to_dict(self):
        self.assertDictEqual(
            Job().to_dict(),
            {'job_id': None, 'user': None, 'status': 0, 'input_name': None,
             'upload_name': None, 'output_name': None, 'model': None,
             'submission_time': None, 'start_time': None,
             'completion_time': None, 'info': '', 'err': '',
             'output_file_url': None}
        )

    def test_invalid_file_dict(self):
        with self.assertRaises(JobCreationError):
            Job().update_in_db()

    def test_from_dict(self):
        self.assertDictEqual(Job.from_dict(self.test_dict).to_dict(),
                             self.test_dict)

    def test_update(self):
        job_id = self.test_job.update_in_db('test-job')

        self.assertEqual(self.test_job.job_id, 'test-job')
        self.assertEqual(job_id, 'test-job')

    def test_from_id(self):
        new_job = Job.from_id('test-job', 'test-user')

        self.assertDictEqual(new_job.to_dict(), self.test_dict)

    def test_from_invalid_id(self):
        with self.assertRaises(JobNotFoundError):
            Job.from_id('invalid-id', 'user')

    def test_non_matching_user(self):
        with self.assertRaises(JobAccessError):
            Job.from_id('test-job', 'incorrect-user')

    def test_delete(self):
        job_to_delete = Job.from_dict(self.test_dict)
        job_to_delete.update_in_db('job-to-delete')

        self.assertTrue(job_to_delete.delete_in_db())

    def test_output_url_unfinished(self):
        self.assertIs(self.test_job.output_file_url, None)

    def tearDown(self) -> None:
        self.test_job.db.document('jobs/test-job').delete()

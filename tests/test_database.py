import unittest
import warnings

from impression_web.database.database_factory import ImpressionDatabaseFactory
from impression_web.job.job_factory import ImpressionJobFactory
from impression_web.job.job import Job


class TestImpressionDatabase(unittest.TestCase):
    user = None
    job_factory = None
    database = None
    jobs = None

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        platform = 'gcp'
        cls.user = 'not-a-user'
        cls.database = ImpressionDatabaseFactory(platform=platform).database()
        job_factory = ImpressionJobFactory(platform=platform)

        cls.jobs = [job_factory.job(user=cls.user,
                                    model='no-model',
                                    job_id=f'test-job-{i + 1}')
                    for i in range(3)]

        [job.update_in_db() for job in cls.jobs]

    def setUp(self) -> None:
        self.user = TestImpressionDatabase.user
        self.database = TestImpressionDatabase.database

    def test_user_jobs(self):
        job_list = list(self.database.user_jobs(self.user))

        self.assertEqual(len(job_list), len(TestImpressionDatabase.jobs),
                         'len(user_jobs) == len(created_jobs)')
        self.assertIsInstance(job_list[0], Job,
                              'job_list[0] is Job')

    def test_user_job_ids(self):
        job_ids = list(self.database.user_job_ids(self.user))

        self.assertEqual(len(job_ids), len(TestImpressionDatabase.jobs),
                         'len(user_job_ids) == len(created_jobs)')
        self.assertListEqual(
            job_ids,
            list(map(lambda x: x.job_id, TestImpressionDatabase.jobs)),
            'matching job ids when fetched from database')

    @classmethod
    def tearDownClass(cls) -> None:
        [job.delete_in_db() for job in cls.jobs]

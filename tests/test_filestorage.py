import pathlib
import unittest
import warnings

from impression_job.storage.file_storage_factory import ImpressionFileStorageFactory
from impression_job.storage.gcp_storage import GCPStorage
from impression_job.storage.exceptions import FileTransferError


class TestImpressionFileStorage(unittest.TestCase):
    storage: GCPStorage = None
    persistent_input = pathlib.PurePath(
        'data/input/test-input-file-2.sdf')
    persistent_output = pathlib.PurePath(
        'data/output/test-output-file-2.sdf')

    @classmethod
    def setUpClass(cls) -> None:
        fs_factory = ImpressionFileStorageFactory(platform='gcp')
        cls.storage = fs_factory.file_storage(
            input_bucket_name='impression-uploads',
            output_bucket_name='impression-output')

        cls.storage.upload_input_file(
            cls.persistent_input)

        cls.storage.upload_output_file(
            cls.persistent_output
        )

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

        self.storage: GCPStorage = TestImpressionFileStorage.storage

        self.test_input_path = pathlib.PurePath(
            'data/input/test-input-file-1.sdf')

        self.test_output_path = pathlib.PurePath(
            'data/output/test-output-file-1.sdf')

    def test_input_upload(self):

        self.storage.upload_input_file(
            self.test_input_path)

        self.assertTrue(
            self.storage._exists(self.storage._input_bucket,
                                 self.test_input_path.name),
            'input file uploaded and present in bucket')

        self.storage.delete_input_file(self.test_input_path.name)

    def test_invalid_input_upload(self):
        with self.assertRaises(FileTransferError):
            self.storage.upload_input_file(
                pathlib.PurePath('data/input/not-a-file.sdf'))

    def test_output_upload(self):
        self.storage.upload_output_file(
            self.test_output_path)

        self.assertTrue(
            self.storage._exists(self.storage._output_bucket,
                                 self.test_output_path.name),
            'input file uploaded and present in bucket')

        self.storage.delete_output_file(self.test_output_path.name)

    def test_invalid_output_upload(self):
        with self.assertRaises(FileTransferError):
            self.storage.upload_output_file(
                pathlib.PurePath('data/out/not-a-file.sdf'))

    def test_double_upload(self):
        self.storage.upload_input_file(
            self.test_input_path)

        self.storage.upload_input_file(
            self.test_input_path)

        self.storage.delete_input_file(self.test_input_path.name)

    def test_input_download(self):
        destination = pathlib.Path('data/test-input-file-2.sdf')
        self.storage.download_input_file(destination)

        self.assertTrue(destination.exists())

        destination.unlink()

    def test_invalid_input_download(self):
        destination = pathlib.Path('not-a-file')
        with self.assertRaises(FileTransferError):
            self.storage.download_input_file(destination)

        try:
            destination.unlink()
        except FileNotFoundError:
            pass

    def test_output_download(self):
        destination = pathlib.Path('data/test-output-file-2.sdf')
        self.storage.download_output_file(destination)

        self.assertTrue(destination.exists())

        destination.unlink()

    def test_invalid_output_download(self):
        destination = pathlib.Path('not-a-file')
        with self.assertRaises(FileTransferError):
            self.storage.download_output_file(destination)

        try:
            destination.unlink()
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.storage.delete_input_file(cls.persistent_input.name)
        cls.storage.delete_output_file(cls.persistent_output.name)

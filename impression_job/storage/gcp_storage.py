"""
GCP Storage class
Manage file upload, download, deletion from relevant buckets
"""
import pathlib

import google.cloud.storage as gc_storage
import google.api_core.exceptions

from impression_job.storage.file_storage import ImpressionFileStorage
from impression_job.storage.exceptions import FileTransferError


class GCPStorage(ImpressionFileStorage):
    """
    Upload, download and delete input/output files
    """
    def __init__(self, input_bucket_name, output_bucket_name):
        self._client: gc_storage.Client = None
        self.input_bucket_name = input_bucket_name
        self.output_bucket_name = output_bucket_name

        self.__input_bucket: gc_storage.Bucket = None
        self.__output_bucket: gc_storage.Bucket = None

    @property
    def client(self):
        if self._client is None:
            self._client = gc_storage.Client()
        return self._client

    @property
    def _input_bucket(self) -> gc_storage.Bucket:
        if self.__input_bucket is None:
            self.__input_bucket = self.client.get_bucket(
                self.input_bucket_name)
        return self.__input_bucket

    @property
    def _output_bucket(self) -> gc_storage.Bucket:
        if self.__output_bucket is None:
            self.__output_bucket = self.client.get_bucket(
                self.output_bucket_name)
        return self.__output_bucket

    def _download_file(self,
                       bucket: gc_storage.Bucket,
                       destination: pathlib.PurePath,
                       file_name: str):
        """
        Download file name (captured from file_path from bucket)
        :param destination: file_path to save file
        :type bucket: :class:`google.cloud.storage.Bucket`
        :param bucket: storage bucket
        :raises: :class: `google.cloud.exception.NotFound`
        """

        file_blob = bucket.blob(file_name)
        try:
            file_blob.download_to_filename(destination.as_posix())
        except google.api_core.exceptions.NotFound:
            raise FileTransferError(
                f'file download failed: {file_name}'
                f'not found in {bucket.name}')

    def _upload_file(self,
                     bucket: gc_storage.Bucket,
                     file_path: pathlib.PurePath,
                     file_name: str):
        """
        Upload file_path to bucket/file_name
        Raises FileTransferError on invalid file path
        """

        blob = bucket.blob(file_name)
        try:
            blob.upload_from_filename(file_path.as_posix())
        except FileNotFoundError:
            raise FileTransferError(
                f'file upload failed: {file_name} not found')

    def _exists(self, bucket: gc_storage.Bucket, file_name: str) -> bool:
        """Does bucket/file_name exist?"""
        blob = bucket.blob(file_name)
        return blob.exists()

    def upload_input_file(self, file_path: pathlib.PurePath,
                          file_name: str = None):
        """Upload file at file_path to input file bucket under its `name`
        :param file_name: name of file in bucket
        :param file_path: file_path to file to be uploaded
        """
        file_name = file_path.name if file_name is None else file_name
        self._upload_file(self._input_bucket, file_path, file_name)

    def download_input_file(self, destination: pathlib.PurePath,
                            file_name: str = None):
        """
        Download file name (captured from file_path from input bucket)
        :param destination: file_path to save file
        :param file_name: name of file in bucket
        :raises: :class: `google.cloud.exception.NotFound`
        """
        file_name = destination.name if file_name is None else file_name
        self._download_file(self._input_bucket, destination, file_name)

    def upload_output_file(self, file_path: pathlib.PurePath,
                           file_name: str = None):
        """
        Upload file at file_path to output file bucket under its `name`
        :param file_path: file_path to file to be uploaded
        :param file_name: name of file in bucket
        """
        file_name = file_path.name if file_name is None else file_name
        self._upload_file(self._output_bucket, file_path, file_name)

    def download_output_file(self, destination,
                             file_name: str = None):
        """
        Download file name (captured from file_path from output bucket)
        :param destination: file_path to save file
        :param file_name: name of file in bucket
        :raises: :class: `google.cloud.exception.NotFound`
        """
        file_name = destination.name if file_name is None else file_name
        self._download_file(self._output_bucket, destination, file_name)

    # todo except invalid file_names
    def delete_input_file(self, file_name: str):
        """
        Delete input_bucket/file_name
        """
        self._input_bucket.delete_blob(file_name)

    # todo except invalid file_names
    def delete_output_file(self, file_name: str):
        """
        Delete output_bucket/file_name
        """
        self._output_bucket.delete_blob(file_name)

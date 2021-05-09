"""
Abstract base class for file storage
"""
import abc
import pathlib


class ImpressionFileStorage(abc.ABC):
    """Manage input and output files within file storage
    Platform agnostic
    """
    @abc.abstractmethod
    def _download_file(self, bucket, dest_path: pathlib.PurePath,
                       file_name: str):
        """Download file_name from bucket to local path"""
        pass

    @abc.abstractmethod
    def _upload_file(self, bucket, file_path: pathlib.PurePath,
                     file_name: str):
        """Upload file at file_path to bucket/file_name"""
        pass

    @abc.abstractmethod
    def upload_input_file(self, file_path: pathlib.PurePath,
                          file_name: str = None):
        """Upload file from file_path to input_bucket/file_name"""
        pass

    @abc.abstractmethod
    def download_input_file(self, dest_file_path: pathlib.PurePath,
                            file_name: str):
        """Download file_name from input_bucket to dest_file_path"""
        pass

    @abc.abstractmethod
    def upload_output_file(self, file_path: pathlib.PurePath,
                           file_name: str = None):
        """Upload file from file_path to output_bucket/file_name"""
        pass

    @abc.abstractmethod
    def download_output_file(self, dest_file_path: pathlib.PurePath,
                             file_name: str):
        """Download file_name from output_bucket to dest_file_path"""
        pass

    @abc.abstractmethod
    def delete_input_file(self, file_name: str):
        """Delete file_name from input_bucket"""
        pass

    @abc.abstractmethod
    def delete_output_file(self, file_name: str):
        """Delete file_name from input_bucket"""
        pass

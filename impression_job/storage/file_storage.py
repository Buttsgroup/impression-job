"""
Abstract base class for file storage
"""
import abc
import pathlib


class ImpressionFileStorage(abc.ABC):
    @abc.abstractmethod
    def _download_file(self, bucket, dest_path: pathlib.PurePath,
                       file_name: str):
        pass

    @abc.abstractmethod
    def _upload_file(self, bucket, file_path: pathlib.PurePath,
                     file_name: str):
        pass

    @abc.abstractmethod
    def upload_input_file(self, file_path: pathlib.PurePath,
                          file_name: str = None):
        pass

    @abc.abstractmethod
    def download_input_file(self, dest_file_path: pathlib.PurePath,
                            file_name: str):
        pass

    @abc.abstractmethod
    def upload_output_file(self, file_path: pathlib.PurePath,
                           file_name: str = None):
        pass

    @abc.abstractmethod
    def download_output_file(self, dest_file_path: pathlib.PurePath,
                             file_name: str):
        pass

    @abc.abstractmethod
    def delete_input_file(self, file_name: str):
        pass

    @abc.abstractmethod
    def delete_output_file(self, file_name: str):
        pass

"""
Creation of platform specific Impression Job instances
"""

from impression_job.job import Job
from impression_job.gc_job import GCPJob


class ImpressionJobFactory:
    def __init__(self, platform):
        self.platform = platform
        self.cls_ = ImpressionJobFactory.select(platform)

    @staticmethod
    def select(platform):
        if platform == 'gcp':
            return GCPJob
        else:
            raise NotImplementedError(
                f'Invalid platform: {platform}')

    def job(self, *args, **kwargs):
        return self.cls_(*args, **kwargs)

    def from_dict(self, *args, **kwargs):
        return self.cls_.from_dict(*args, **kwargs)

    def from_id(self, *args, **kwargs):
        return self.cls_.from_id(*args, **kwargs)

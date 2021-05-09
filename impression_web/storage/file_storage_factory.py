"""
Factory for platform specific FileStorage instances
"""
from impression_web.storage.gcp_storage import GCPStorage


class ImpressionFileStorageFactory:
    def __init__(self, platform):
        self.platform = platform
        self.cls_ = ImpressionFileStorageFactory._select(platform)

    @staticmethod
    def _select(platform):
        if platform == 'gcp':
            return GCPStorage
        else:
            raise NotImplementedError(
                f'Invalid platform: {platform}')

    def file_storage(self, *args, **kwargs):
        return self.cls_(*args, **kwargs)

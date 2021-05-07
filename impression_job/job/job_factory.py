from impression_job.job.gcp_job import GCPJob


class ImpressionJobFactory:
    """
    Create platform specific Job objects
    directly (job)
    from dictionary (from_dict)
    from id (database job id)
    """
    def __init__(self, platform):
        self.platform = platform
        self.cls_ = ImpressionJobFactory._select(platform)

    @staticmethod
    def _select(platform):
        """Return the platform specific Job class"""
        if platform == 'gcp':
            return GCPJob
        else:
            raise NotImplementedError(
                f'Invalid platform: {platform}')

    def job(self, *args, **kwargs):
        """Platform specific Job creation"""
        return self.cls_(*args, **kwargs)

    def from_dict(self, *args, **kwargs):
        return self.cls_.from_dict(*args, **kwargs)

    def from_id(self, *args, **kwargs):
        return self.cls_.from_id(*args, **kwargs)
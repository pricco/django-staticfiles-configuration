from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from django.contrib.staticfiles.storage import CachedFilesMixin
from django.contrib.staticfiles.finders import get_finders
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class StaticStorage(CachedFilesMixin, S3BotoStorage):
    """ Static files storage.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            bucket=settings.STATIC_BUCKET,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            headers=settings.STATIC_HEADERS,
            location=settings.STATIC_LOCATION,
            custom_domain=settings.STATIC_DOMAIN,
            gzip=False)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def exists(self, name):
        # TODO: We should improve post_process instead of override this
        return self.local_storage.exists(name) and super().exists(name)

    def _save(self, name, content):
        name = super()._save(name, content)
        self.local_storage._save(name, content)
        return name


class CompressStorage(StaticStorage):

    def save(self, name, content):
        name = super().save(name, content)
        matches = lambda path: matches_patterns(path, self._patterns.keys())
        storage = FileSystemStorage()
        for finder in get_finders():
            path = finder.find(name)
            if path:
                processor = self.post_process({name: (storage, path)})
                for original_path, processed_path, processed in processor:
                    if isinstance(processed, Exception):
                        print(processed)
                break
        return name

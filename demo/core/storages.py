import os
import re
from collections import OrderedDict

from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import CachedFilesMixin
from django.contrib.staticfiles.utils import check_settings, matches_patterns
from django.contrib.staticfiles.finders import get_finders
from django.utils.encoding import force_bytes, force_text
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage
from compressor.storage import  CompressorFileStorage


HASHED = re.compile(r'\.[0-9abcdef]{12}\.')


class FakeCompressorFileStorage(CompressorFileStorage):
    """ Use only for development (DEBUG=True)
    """

    def exists(self, name):
        """ Avoid cached scss file
        """
        if name.endswith('.scss'):
            return False
        return super().exists(name)


class StaticStorage(CachedFilesMixin, S3BotoStorage):
    """ Static files storage.
    """
    patterns = CachedFilesMixin.patterns + (
        ("*.scss", (
            r"""(url\(['"]{0,1}\s*(.*?)["']{0,1}\))""",
        )),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            bucket=settings.STATIC_BUCKET,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            headers=settings.STATIC_HEADERS,
            location=settings.STATIC_LOCATION,
            custom_domain=settings.STATIC_DOMAIN,
            gzip=False)
        # Django compressor uses local files
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def exists(self, name):
        """ Check if file exists locally
        """
        return self.local_storage.exists(name)

    def _save(self, name, content):
        """ Save to local too (improve perfomance)
        """
        name = super()._save(name, content)
        self.local_storage._save(name, content)
        return name

    def _open(self, name, mode='rb'):
        """ Open from local (improve perfomance)
        """
        return self.local_storage._open(name, mode)

    def post_process(self, paths, dry_run=False, **options):
        """ Copy from CachedFilesMixin
            https://code.djangoproject.com/ticket/19670
        """
        # don't even dare to process the files if we're in dry run mode
        if dry_run:
            return

        # where to store the new paths
        hashed_files = OrderedDict()

        # build a list of adjustable files
        matches = lambda path: matches_patterns(path, self._patterns.keys())
        adjustable_paths = [path for path in paths if matches(path)]

        # then sort the files by the directory level
        path_level = lambda name: len(name.split(os.sep))
        for name in sorted(paths.keys(), key=path_level, reverse=True):

            # use the original, local file, not the copied-but-unprocessed
            # file, which might be somewhere far away, like S3
            storage, path = paths[name]
            with storage.open(path) as original_file:

                # generate the hash with the original content, even for
                # adjustable files.
                hashed_name = self.hashed_name(name, original_file)

                # then get the original's file content..
                if hasattr(original_file, 'seek'):
                    original_file.seek(0)

                hashed_file_exists = self.exists(hashed_name)
                processed = False

                # ..to apply each replacement pattern to the content
                if name in adjustable_paths:
                    content = original_file.read().decode(settings.FILE_CHARSET)
                    for extension, patterns in self._patterns.items():
                        if matches_patterns(path, (extension,)):
                            for pattern, template in patterns:
                                converter = self.url_converter(name, template)
                                try:
                                    content = pattern.sub(converter, content)
                                except ValueError as exc:
                                    yield name, None, exc
                    if hashed_file_exists:
                        self.delete(hashed_name)
                    # then save the processed result
                    content_file = ContentFile(force_bytes(content))
                    saved_name = self._save(hashed_name, content_file)
                    hashed_name = force_text(self.clean_name(saved_name))
                    processed = True
                else:
                    # or handle the case in which neither processing nor
                    # a change to the original file happened
                    if not hashed_file_exists:
                        processed = True
                        saved_name = self._save(hashed_name, original_file)
                        hashed_name = force_text(self.clean_name(saved_name))

                # and then set the cache accordingly
                hashed_files[self.hash_key(name)] = hashed_name
                yield name, hashed_name, processed

        # Finally store the processed paths
        self.hashed_files.update(hashed_files)

    def url_converter(self, name, template=None):
        # Change name to resolve urls for scss files (assume /css directory)
        if name.endswith('.scss'):
            name = 'css/fake.css'
        base_converter = super().url_converter(name, template)
        def converter(matchobj):
            matched, url = matchobj.groups()
            # If url is already hashed exit
            if HASHED.search(url):
                return matched
            return base_converter(matchobj)
        return converter


class CompressorStorage(StaticStorage):

    def save(self, name, content):
        name = super().save(name, content)
        storage = FileSystemStorage(
            location=settings.STATIC_ROOT,
            base_url=settings.STATIC_URL)
        for finder in get_finders():
            path = finder.find(name)
            if path:
                print(path)
                processor = self.post_process({name: (self, path)})
                for original_path, processed_path, processed in processor:
                    if isinstance(processed, Exception):
                        print(processed)
                break
        return name

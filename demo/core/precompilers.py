import sass
import os

from django.contrib.staticfiles.finders import find
from django.apps.registry import apps
from django.conf import settings


include_paths = None


def get_scss_include_paths():
    global include_paths
    if include_paths is None:
        base = find('.', all=True)
        if settings.STATIC_ROOT:
            static_root = os.path.abspath(settings.STATIC_ROOT)
            base = filter(lambda x: not x.startswith(static_root), base)
        include_paths = ':'.join(base)
    return include_paths


class ScssFilter(object):

    def __init__(self, content, type, *args, **kwargs):
        self.path = os.path.dirname(kwargs.get('filename'))
        self.content = content
        self.type = type

    def input(self, **kwargs):
        return sass.compile_string(
            self.content.encode(),
            ':'.join([self.path, get_scss_include_paths()]).encode()
        ).decode()

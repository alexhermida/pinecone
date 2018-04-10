import os
import platform

from .base import *  # noqa: F401,F403

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = [
    '.vigotech.org',
    '.xip.io',
]
ADMINS = (('VigoTech', 'alliance@vigotech.org'),)
EMAIL_SUBJECT_PREFIX = '[alliance@{}] '.format(platform.node())

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django settings for example project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os, sys
APP = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = dict(
    default=dict(
        ENGINE='django.db.backends.sqlite3',
        NAME='dev.db',
        USER='',
        HOST='',
        PORT='',
    ),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join('media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g2_39yupn*6j4p*cg2%w643jiq-1n_annua*%i8+rq0dx9p=$n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'iris.example.middleware.OverrideUserMiddleware',
    )

ROOT_URLCONF = 'iris.example.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTHENTICATION_BACKENDS = (
    'iris.example.backends.ContrivedBackend',
    'django.contrib.auth.backends.ModelBackend',
)

IRIS_ITEM_TYPE_PLUGINS = (
    'iris.plugins.ParticipantAddUserPlugin',
    'iris.example.plugins.OneLinerAddPlugin',
    'iris.example.plugins.NoteAddPlugin',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'iris',
    'iris.example',
    'south',
)

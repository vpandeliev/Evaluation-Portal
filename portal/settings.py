#Django settings for portal project.
import os
import sys

ROOT_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.normpath(os.path.join(ROOT_PATH, "../lib")))
sys.path.insert(0, os.path.normpath(os.path.join(ROOT_PATH,"..")))
#print sys.path
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SESSION_COOKIE_AGE = 1209600
ADMINS = (
    ('Velian Pandeliev', 'vpandeliev@gmail.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

FIXTURE_DIRS = (
    #'../fixtures/'
)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    #'studies.context_processors.msgproc'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
		
    # 'lockdown.middleware.LockdownMiddleware',
)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

INSTALLED_APPS = (
	'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'portal.studies',
    
    # Hosted games
    #'portal.assess',
    'portal.assess',
    'portal.boggle',
    'portal.rushhour',
    'portal.tutorial_study',
    'portal.study_builder',
    # Libraries
   'tinymce',
#	'lockdown',
	'alphacabbage.django.helpers',
	'alphacabbage.django.choices',
)

try:
    from portal.local_settings import *
except ImportError:
    print u'File local_settings.py is not found. Continuing with production settings.'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media/')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/amedia/'

TEMPLATE_DIRS = (
	os.path.join(ROOT_PATH, 'templates'),
	os.path.join(ROOT_PATH, 'templates/study'),
	#os.path.join(ROOT_PATH, 'templates/registration'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


MEDIA_URL = '/media/' 

#try:
#    from local_settings import *
#except ImportError:
#    print u'File local_settings.py is not found. Continuing with production settings.'

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
		'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifyfull,|cut,copy,paste,pastetext,|,undo,redo,|,link,unlink,anchor,image,search,replace,|,bullist,numlist,|,cleanup,help,code,|,insertdate,inserttime,preview",
		'theme_advanced_buttons2' : "",
		'theme_advanced_buttons3': '',
		'theme_advanced_toolbar_location' : "top",
		'theme_advanced_toolbar_align' : "left",
		'theme_advanced_statusbar_location' : "bottom",
		'theme_advanced_resizing' : 'True',
}

JS_URL = '%sjs/tiny_mce/tiny_mce.js' % MEDIA_URL
JS_ROOT = os.path.join(MEDIA_ROOT, 'js/tiny_mce')
ROOT_URLCONF = 'portal.urls'

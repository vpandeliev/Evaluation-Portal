
from cache_settings import *

try:
    from local_settings import *
except ImportError:
    print u'File custom_settings/local_settings.py is not found. Continuing with production settings.'

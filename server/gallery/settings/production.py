from defaults import *
import os.path


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

STATIC_ROOT = os.path.join('usr', 'local', 'gallery', 'static')

from defaults import *
import os.path


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

STATIC_ROOT = os.path.join(os.path.abspath(os.sep), 'usr', 'local', 'gallery', 'static')

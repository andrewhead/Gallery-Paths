from defaults import *
import os.path


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

STATIC_ROOT = os.path.join(os.path.abspath(os.sep), 'usr', 'local', 'gallery', 'static')

ALLOWED_HOSTS = [
    '.gallerypaths.com',
    '.gallerypaths.com.',
]

LOGGING = {
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/gallery.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        }
        'gallery': {
            'handlers': ['file'],
            'level': 'DEBUG',
         },
    }
}

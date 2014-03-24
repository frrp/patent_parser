import os


normpath = lambda *args: os.path.normpath(os.path.abspath(os.path.join(*args)))


PROJECT_ROOT = normpath(__file__, "../..")

ALLOWED_HOSTS = ()
DEBUG = True
SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(PROJECT_ROOT, "db", "default.db")
    }
}
MEDIA_ROOT = normpath(PROJECT_ROOT, "static", "uploads")
MEDIA_URL = '/static/uploads/'
STATIC_ROOT = normpath(PROJECT_ROOT, "static", "static")
STATIC_URL = '/static/static/'
SECRET_KEY = "asdfghjkl"
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'wsgi.application'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',

    "large_data_admin",
    'tastypie',

    "sucker",
)


TEMP = normpath(PROJECT_ROOT, "tmp")

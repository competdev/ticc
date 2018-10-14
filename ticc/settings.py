import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'rc%r*4pmo7&i^a2b@lsfp(cmxv5@3fcdd+ufq0j*clesun^0zo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.cefetmg.br', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'website.apps.WebsiteConfig',
    'rankings.apps.RankingsConfig',
    'captcha',
	'chartjs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ticc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticc.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ticc',
        'USER': 'luis',
        'PASSWORD': 'op',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/login'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

DATE_INPUT_FORMATS = ("%d/%m/%Y", )

RECAPTCHA_PUBLIC_KEY = '6LfVoCYTAAAAAH3rX3laFwniK21XMcKISfo31pbM'
RECAPTCHA_PRIVATE_KEY = '6LfVoCYTAAAAABDstANhXJFfJEZocLvgWxjitqSe'
NOCAPTCHA = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
}

INTERNAL_IPS = ['127.0.0.1', 'localhost']

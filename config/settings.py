from pathlib import Path
import os, secrets
BASE_DIR = Path(__file__).resolve().parent.parent
# Generate a local key once; deliberately excluded from the downloadable project.
key_file = BASE_DIR / '.local-secret'
if not key_file.exists():
    key_file.write_text(secrets.token_urlsafe(50))
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or key_file.read_text().strip()
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
INSTALLED_APPS = ['django.contrib.staticfiles', 'shop']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors':
              ['django.template.context_processors.request']}}]
DATABASES = {}  # No models, migrations, admin, or login required.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

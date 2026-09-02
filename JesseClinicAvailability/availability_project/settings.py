from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "interview-only-not-for-production"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "scheduling",
]

MIDDLEWARE = []
ROOT_URLCONF = "availability_project.urls"
TEMPLATES = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

TIME_ZONE = "Europe/London"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


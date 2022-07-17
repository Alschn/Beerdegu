"""
Configuration for collecting static files in Dockerfile.prod.
Do not use as runtime settings. Server should be running with `core.settings.prod`!
"""
from core.settings.base import *

ALLOWED_HOSTS = []

ROOT_DIR = BASE_DIR.parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

TEMPLATES[0]["DIRS"] = [os.path.join(ROOT_DIR, "frontend", "build")]

STATICFILES_DIRS = [os.path.join(ROOT_DIR, "frontend", "build", "static")]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")

STATIC_URL = "/static/"

WHITENOISE_ROOT = os.path.join(ROOT_DIR, "frontend", "build", "root")

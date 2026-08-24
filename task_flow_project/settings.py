# task_flow_project/settings.py
#
# Django's central configuration file. Every app in the project (like our
# "tasks" app) is registered here, and this is where the database
# connection, security settings, and template locations are all defined.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file during development

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Pulled from the environment rather than hardcoded — see .env.example.
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-dev-key-do-not-use-in-production")

# SECURITY WARNING: don't run with DEBUG turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

# In production, set this to your actual domain(s), e.g. ["taskflow.com"]
ALLOWED_HOSTS = ["*"] if DEBUG else os.environ.get("ALLOWED_HOSTS", "").split(",")

# Application definition — every Django "app" (self-contained module) must
# be listed here for Django to recognize its models, templates, etc.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",  # our own app, defined in tasks/
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "task_flow_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Django auto-discovers templates inside each app's templates/ folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_flow_project.wsgi.application"

# Database
# Parses DATABASE_URL (e.g. "postgresql://user:pass@host:5432/dbname")
# into the dictionary format Django's DATABASES setting expects.
import dj_database_url  # noqa: E402 — imported here to keep it near its one use

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

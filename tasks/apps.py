# tasks/apps.py
#
# Django's app configuration. Boilerplate that Django generates for every
# app — it's what lets INSTALLED_APPS in settings.py refer to "tasks".

from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"

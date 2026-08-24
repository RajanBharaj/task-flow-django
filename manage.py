#!/usr/bin/env python
"""manage.py — Django's command-line utility for administrative tasks.

Common commands you'll use with this file:
  python manage.py runserver        # start the local dev server
  python manage.py migrate          # apply database migrations
  python manage.py makemigrations   # generate new migrations from models.py changes
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_flow_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

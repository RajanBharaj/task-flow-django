# tasks/models.py
#
# Django's ORM lets us define the database table in plain Python.
# Running "python manage.py makemigrations" generates a migration file
# from this class, and "python manage.py migrate" applies it to turn
# this into an actual Postgres table.

from django.db import models


class Task(models.Model):
    """A single task in the tracker."""

    title = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tasks"          # explicit snake_case table name
        ordering = ["-created_at"]  # newest first, by default

    def __str__(self):
        # Controls how a Task displays in Django's admin panel and shell —
        # e.g. "Task object (1)" becomes "Buy milk" instead.
        return self.title

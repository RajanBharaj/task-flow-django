# tasks/urls.py
#
# URL routes specific to the "tasks" app. Registered into the project via
# task_flow_project/urls.py's include("tasks.urls").

from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("create/", views.task_create, name="task_create"),
]

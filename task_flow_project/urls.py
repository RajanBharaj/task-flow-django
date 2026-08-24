# task_flow_project/urls.py
#
# The project-wide URL router. This file delegates everything under the
# root path ("") to our "tasks" app's own urls.py — keeping each app's
# routes self-contained rather than listing every route in one giant file.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),  # delegate to tasks/urls.py
]

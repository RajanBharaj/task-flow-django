# tasks/views.py
#
# Views handle the request/response cycle. Notice there's no separate
# "API endpoint" here — the same view renders HTML directly, and HTMX
# (in our templates) treats that HTML as the response to swap into the page.

from django.shortcuts import render
from .models import Task


def task_list(request):
    """
    Renders the full page on a normal GET request (e.g. the first time
    a visitor loads the site).
    """
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_create(request):
    """
    Handles the "Add Task" form submission.

    Because this is called by HTMX (not a full page reload), we return
    only the updated task list *fragment* — HTMX swaps it into the page
    in place, without a full browser navigation.
    """
    title = request.POST.get("title", "").strip()

    if title:
        Task.objects.create(title=title)

    tasks = Task.objects.all()
    return render(request, "tasks/task_list_partial.html", {"tasks": tasks})

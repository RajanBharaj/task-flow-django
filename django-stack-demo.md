# TaskFlow — Django + PostgreSQL + HTMX Demo

This demo uses **HTMX** rather than React for the frontend half of "React/HTMX" —
deliberately, because it showcases a fundamentally different (and increasingly
popular) philosophy: **the server renders HTML, and HTMX swaps fragments of it
into the page** — no client-side JavaScript framework, no separate frontend
build step, no JSON API layer at all.

## Project structure
```
task_flow_django/
├── tasks/                        # Django "app" (a self-contained module)
│   ├── models.py                 # Database model
│   ├── views.py                  # Request handlers
│   ├── urls.py                   # URL routes for this app
│   └── templates/
│       └── tasks/
│           ├── task_list.html    # Full page
│           └── task_list_partial.html  # Just the <ul> — HTMX swaps this in
└── task_flow_project/
    └── urls.py                   # Project-wide URL routing
```

---

### `tasks/models.py`
Django's ORM defines the model in plain Python. Migrations (auto-generated
from this file) handle turning it into actual Postgres tables/columns.

```python
# tasks/models.py

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
        return self.title
```

---

### `tasks/views.py`
Views handle the request/response cycle. Notice there's no separate "API
endpoint" — the same view renders HTML directly, and HTMX treats that HTML
as the response to swap into the page.

```python
# tasks/views.py

from django.shortcuts import render
from .models import Task


def task_list(request):
    """
    Renders the full page on a normal GET request.
    """
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_create(request):
    """
    Handles the "Add Task" form submission.

    Because this is called by HTMX (not a full page reload), we return only
    the updated task list fragment — HTMX swaps it into the page in place.
    """
    title = request.POST.get("title", "").strip()

    if title:
        Task.objects.create(title=title)

    tasks = Task.objects.all()
    return render(request, "tasks/task_list_partial.html", {"tasks": tasks})
```

---

### `tasks/urls.py`
```python
# tasks/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("create/", views.task_create, name="task_create"),
]
```

---

### `tasks/templates/tasks/task_list.html`
The full page, loaded once. It pulls in HTMX from a CDN — no `npm install`,
no bundler.

```html
<!-- tasks/templates/tasks/task_list.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TaskFlow</title>
  <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body style="max-width: 480px; margin: 2rem auto; font-family: sans-serif;">
  <h1>TaskFlow</h1>

  <!--
    hx-post: where to send the form on submit
    hx-target: which element on the page gets replaced with the response
    hx-swap: how to insert it ("outerHTML" replaces the target element itself)
    This entirely replaces the need for onSubmit + fetch + setState in React.
  -->
  <form hx-post="{% url 'task_create' %}"
        hx-target="#task-list-container"
        hx-swap="outerHTML">
    {% csrf_token %}
    <input type="text" name="title" placeholder="What needs doing?" required>
    <button type="submit">Add Task</button>
  </form>

  {% include "tasks/task_list_partial.html" %}
</body>
</html>
```

---

### `tasks/templates/tasks/task_list_partial.html`
A fragment — just the list. This is what `task_create` returns, and what
HTMX swaps into `#task-list-container`. Reused by both the full page (via
`{% include %}`) and the HTMX response, so the list markup only lives in one place.

```html
<!-- tasks/templates/tasks/task_list_partial.html -->
<ul id="task-list-container">
  {% for task in tasks %}
    <li style="text-decoration: {% if task.is_complete %}line-through{% else %}none{% endif %};">
      {{ task.title }}
    </li>
  {% empty %}
    <li>No tasks yet — add one above.</li>
  {% endfor %}
</ul>
```

## What this demonstrates
- **No API layer needed**: `task_create` returns HTML, not JSON — there's nothing equivalent to `route.ts` or `task-routes.js` translating data into a format the frontend then re-renders.
- **Batteries included**: Django's ORM (`Task.objects.all()`), CSRF protection (`{% csrf_token %}`), and templating are all built in — compare to MERN, where Mongoose, CORS, and JSON parsing were each separate decisions/packages.
- **Progressive enhancement**: the form still works (via full page reload) even if HTMX fails to load, since it's a real `<form>` posting to a real URL — a resilience property neither of the other two demos have by default.
- **Template reuse**: `task_list_partial.html` is shared between the initial page load and every subsequent HTMX update, so the "what a task looks like" markup exists in exactly one file.

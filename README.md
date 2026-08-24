# TaskFlow — Django + PostgreSQL + HTMX

A minimal task tracker demonstrating a fundamentally different philosophy
from the other two demos: **the server renders HTML directly, and HTMX
swaps fragments of it into the page** — no client-side JavaScript framework,
no separate frontend build, no JSON API layer at all.

## Project structure
```
task-flow-django/
├── task_flow_project/       # Django "project" — site-wide configuration
│   ├── settings.py          # Database, installed apps, templates config
│   ├── urls.py               # Project-wide URL routing
│   ├── wsgi.py                # Entry point for production servers (gunicorn)
│   └── asgi.py
├── tasks/                    # Django "app" — a self-contained module
│   ├── models.py              # The Task database model
│   ├── views.py                # Request handlers
│   ├── urls.py                  # URL routes for this app
│   └── templates/tasks/
│       ├── task_list.html        # Full page
│       └── task_list_partial.html # Just the <ul> — what HTMX swaps in
├── manage.py                 # Django's command-line utility
├── requirements.txt
└── .env.example
```

## Run it locally

1. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up your database**

   Copy `.env.example` to `.env` and fill in a real Postgres connection
   string (e.g. from [Render](https://render.com) or [Neon](https://neon.tech)),
   or leave `DATABASE_URL` unset to use a local SQLite file for quick testing.
   ```bash
   cp .env.example .env
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the dev server**
   ```bash
   python manage.py runserver
   ```
   Visit http://localhost:8000

## Deploying

This project deploys well to **Render**, which can host the Django app
and a managed Postgres database in one dashboard:

1. Push this folder to a GitHub repo.
2. Create a new **Web Service** on Render, point it at the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn task_flow_project.wsgi`
5. Add a Render **Postgres** database and copy its connection string into
   the `DATABASE_URL` environment variable on the web service.
6. Set `SECRET_KEY` to a real generated value and `DEBUG=False`.

## What this demonstrates

- **No API layer needed**: `task_create` in `views.py` returns HTML, not
  JSON — there's nothing equivalent to the `route.ts` or `task-routes.js`
  files from the other two demos, translating data into a format the
  frontend then has to re-render.
- **Batteries included**: Django's ORM (`Task.objects.all()`), CSRF
  protection (`{% csrf_token %}`), and templating are all built in.
- **Progressive enhancement**: the form is a real `<form>` posting to a
  real URL — it still works via a full page reload even if HTMX fails to
  load, a resilience property neither of the other two demos have by default.
- **Template reuse**: `task_list_partial.html` is shared between the
  initial page load (via `{% include %}`) and every subsequent HTMX
  update, so the "what a task looks like" markup exists in exactly one file.

# task_flow_project/wsgi.py
#
# WSGI entry point used by production servers like gunicorn to run the app.
# (Render/Railway will run something like: gunicorn task_flow_project.wsgi)

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_flow_project.settings")

application = get_wsgi_application()

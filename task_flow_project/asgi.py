# task_flow_project/asgi.py
#
# ASGI entry point — used if you later add async features (websockets,
# background tasks). Not required for this simple demo, but Django
# generates it by convention.

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_flow_project.settings")

application = get_asgi_application()

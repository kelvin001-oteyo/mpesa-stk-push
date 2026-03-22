import os
from django.core.wsgi import get_wsgi_application

# ✅ FIXED SETTINGS PATH
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings')

application = get_wsgi_application()

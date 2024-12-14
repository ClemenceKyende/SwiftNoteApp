import os
import sys

# Add your project directory to the sys.path
path = '/home/ClemenceKyende/swiftnote'  # Update with the correct path
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiftnote.settings')

application = get_wsgi_application()

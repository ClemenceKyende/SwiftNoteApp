import os
import sys

# Add your project directory to the sys.path
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')  # Automatically adds the project root
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiftnote.settings')

application = get_wsgi_application()

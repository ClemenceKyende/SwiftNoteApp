release: python manage.py collectstatic --noinput
web: waitress-serve --listen=0.0.0.0:8000 swiftnote.wsgi:application

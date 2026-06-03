"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

if os.getenv('VERCEL'):
    from django.core.management import call_command

    call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)

# Vercel's Python runtime looks for a WSGI callable named `app`.
app = application

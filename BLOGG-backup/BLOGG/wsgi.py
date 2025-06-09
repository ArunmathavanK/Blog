"""
WSGI config for BLOGG project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BLOGG.settings')
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env.production')
load_dotenv(dotenv_path=env_path)
application = get_wsgi_application()
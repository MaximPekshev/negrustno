# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0872810/data/www/negrustno.ru/negrustno')
sys.path.insert(1, '/var/www/u0872810/data/negrustnoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'negrustno.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
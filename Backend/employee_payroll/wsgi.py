"""
WSGI config for employee_payroll project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_payroll.settings')
application = get_wsgi_application()

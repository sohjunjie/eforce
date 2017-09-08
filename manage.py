#!/usr/bin/env python
import os
import sys
import dotenv

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eforce.settings")

    from django.core.management import execute_from_command_line

    is_testing = 'test' in sys.argv
    if is_testing:
        import coverage
        cov = coverage.coverage(source=['eforce_api', ], omit=['*/tests/*', '*/migrations/*'])
        cov.set_option('report:show_missing', True)
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys, logging


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


logging.basicConfig(format='%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d] %(message)s', datefmt='%d-%m-%Y '
                                                                                                       '%H:%M:%S ',
                    level=logging.CRITICAL,
                    filename='logs.txt')
logger = logging.getLogger('userathlogs')

if __name__ == '__main__':
    main()

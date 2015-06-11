#!/usr/bin/env python
"""import imp

from django.core.management import execute_manager

import settings


try:
    imp.find_module('settings')  # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)


if __name__ == "__main__":
    execute_manager(settings)
"""

import os
import sys

if __name__ == "__main__":
    #get the source name here
    source_path=os.getcwd()
    content_root=os.path.realpath(os.path.join(source_path,os.pardir))
    sys.path.append(source_path)
    sys.path.append(content_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebServer.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

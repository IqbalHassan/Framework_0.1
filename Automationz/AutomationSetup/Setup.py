# Copyright 2015, Automation Solutionz
# ---

import subprocess
#import webbrowser
#from zipfile import *


install_str = "pip install"
#server_zip_file = "test.zip"

# Installation function
def install(type = "", module_name = "", module_version = None, cmd = ""):
    command = ""
    
    if type == "pip":
        command = "%s %s" % (install_str, module_name)
        if module_version:
            command = "%s==%s" % (command, module_version)
    else:
        command = cmd
    
    subprocess.call(command, shell=True)

# Test command execution
# install(cmd = "dir")

# Webpage open
"""def open_webpage(url):
    if url:
        webbrowser.open(url, new=2)

# ---

# Navigate to PostgreSQL download
open_webpage("http://www.enterprisedb.com/products-services-training/pgdownload#windows")


raw_input("Finished downloading and installing PostgreSQL? [Press \"Enter\" to confirm]")"""


# Check and install django
django_version = "1.5"
try:
    import django
except ImportError as e:
    install(type="pip", module_name="django", module_version="1.5")


# Check and install django-celery
"""try:
    import django-celery
except ImportError as e:"""
install(type="pip", module_name="django-celery")


# Check and install selenium
try:
    import selenium
except ImportError as e:
    install(type="pip", module_name="selenium")



# Check and install psutil
try:
    import psutil
except ImportError as e:
    install(type="pip", module_name="psutil")
    

# Check and install wmi
try:
    import wmi
except ImportError as e:
    install(type="pip", module_name="wmi")


# Check and install requests
try:
    import requests
except ImportError as e:
    install(type="pip", module_name="requests")
    
# Check and install six
try:
    import six
except ImportError as e:
    install(type="pip", module_name="six")

# Check and install pillow
try:
    import Pillow
except ImportError as e:
    install(type="pip", module_name="Pillow")




# Check and install poster
try:
    import poster
except ImportError as e:
    install(type="pip", module_name="poster")

# Check and install psycopg2
try:
    import psycopg2
except ImportError as e:
    psycopg2_easy_install = "easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.0/psycopg2-2.6.0.win32-py2.7-pg9.4.1-release.exe"
    install(cmd=psycopg2_easy_install)

# Check and install win32api
try:
    import win32api
except ImportError as e:
    win32api_easy_install = "easy_install http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download"
    install(cmd=win32api_easy_install)


# Check and install dateutil.relativedelta 
try:
    from dateutil.relativedelta import relativedelta
except ImportError as e:
    relativedelta_easy_install = "easy_install https://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz"
    install(cmd=relativedelta_easy_install)


#pill
#http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
try:
    from PIL import ImageGrab
except ImportError as e:
    PIL_easy_install = "easy_install http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe"
    install(cmd=PIL_easy_install)
# Extract the zip file containing the server
# https://docs.python.org/2/library/zipfile.html
"""with ZipFile(server_zip_file, "r") as zf:
    zf.extractall()"""

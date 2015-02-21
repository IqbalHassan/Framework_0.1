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
    


# Check and install poster
try:
    import poster
except ImportError as e:
    install(type="pip", module_name="poster")

# Check and install psycopg2
try:
    import psycopg2
except ImportError as e:
    psycopg2_pip_uri = "pip install git+https://github.com/nwcell/psycopg2-windows.git@win64-py27#egg=psycopg2"
    install(cmd=psycopg2_pip_uri)


# Extract the zip file containing the server
# https://docs.python.org/2/library/zipfile.html
"""with ZipFile(server_zip_file, "r") as zf:
    zf.extractall()"""

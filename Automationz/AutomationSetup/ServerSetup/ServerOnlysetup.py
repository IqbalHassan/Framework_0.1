# Copyright 2015, Automation Solutionz
# ---

import subprocess
import webbrowser
from zipfile import *

path= "C:\Python27\Lib\site-packages"
install_str = "pip install"
server_zip_file = "test.zip"

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
def open_webpage(url):
    if url:
        webbrowser.open(url, new=2)

# ---

# Navigate to PostgreSQL download
open_webpage("http://www.enterprisedb.com/products-services-training/pgdownload#windows")


raw_input("Finished downloading and installing PostgreSQL? [Press \"Enter\" to confirm]")


# Check and install django
django_version = "1.8.2"
try:
    import django
except ImportError as e:
    install(type="pip", module_name="django", module_version="1.8.2")

# Check and install wheel
try:
    import wheel
except ImportError as e:
    psycopg2_pip_uri = "pip install wheel -t "+path
    install(cmd=psycopg2_pip_uri)

# Check and install psycopg2
try:
    import psycopg2
except ImportError as e:
	psycopg2_pip_uri = "pip install wheel RequiredFiles\psycopg2-2.5.5-cp27-none-win32.whl"
	install(cmd=psycopg2_pip_uri)
try:
	import simplejson
except ImportError as e:
	simplejson_command="pip install git+https://github.com/simplejson/simplejson.git"
	install(cmd=simplejson_command)

# Extract the zip file containing the server
# https://docs.python.org/2/library/zipfile.html
with ZipFile(server_zip_file, "r") as zf:
    zf.extractall()

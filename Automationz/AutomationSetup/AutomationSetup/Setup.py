# Copyright 2015, Automation Solutionz
# ---

import subprocess
#import webbrowser
#from zipfile import *


install_str = "pip install -U"
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

# Check and install django
django_version = "1.5"
try:
    install(type="pip", module_name="django", module_version=django_version)
except:
    print "unable to install/update django" 


# Check and install django-celery

try:
    install(type="pip", module_name="django-celery")
except:
    print "unable to install/update django-celery" 

# Check and install selenium
try:
    install(type="pip", module_name="selenium")
except:
    print "unable to install/update selenium"

# Check and install psutil
try:
    install(type="pip", module_name="psutil")
except:
    print "unable to install/update psutil"

# Check and install wmi
try:
    install(type="pip", module_name="wmi")
except:
    print "unable to install/update psutil"

# Check and install requests
try:
    install(type="pip", module_name="requests")
except:
    print "unable to install/update psutil"
    
# Check and install six
try:
    install(type="pip", module_name="six")
except:
    print "unable to install/update psutil"

# Check and install pillow
try:
    install(type="pip", module_name="Pillow")
except:
    print "unable to install/update psutil"

# Check and install poster
try:
    install(type="pip", module_name="poster")
except:
    print "unable to install/update psutil"

# Check and install psycopg2
try:
    import psycopg2
except ImportError as e:
    try:
        psycopg2_easy_install = "easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.0/psycopg2-2.6.0.win32-py2.7-pg9.4.1-release.exe"
        install(cmd=psycopg2_easy_install)
    except:
        print "unable to install/update psycopg2"
# Check and install win32api
try:
    import win32api
except ImportError as e:
    try: 
        win32api_easy_install = "easy_install http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download"
        install(cmd=win32api_easy_install)
    except:
        print "unable to install/update win32api"

# Check and install dateutil.relativedelta 
try:
    from dateutil.relativedelta import relativedelta
except ImportError as e:
    try:
        relativedelta_easy_install = "easy_install https://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz"
        install(cmd=relativedelta_easy_install)
    except:
        print "unable to install/update relativedelta"

#pill
#http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
try:
    from PIL import ImageGrab
except ImportError as e:
    try:
        PIL_easy_install = "easy_install http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe"
        install(cmd=PIL_easy_install)
    except:
        print "unable to install/update ImageGrab"



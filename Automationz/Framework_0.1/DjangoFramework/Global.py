<<<<<<< HEAD
# -*- coding: cp1252 -*-
import os
import time


###########Production / Dev Config variables######################
#Environment = "Production"
Environment = "Test"

def get_ip():
    if Environment == "Test":
        print "Running on Test Environment..."
        return "127.0.0.1"
    elif Environment == "Production":
        print "Running on Production Environment..."
        return "135.23.123.67"

def set_debug():
    if Environment == "Test":
        debug_value = True
        return debug_value
    elif Environment == "Production":
        debug_value = False
=======
# -*- coding: cp1252 -*-
import os
import time


###########Production / Dev Config variables######################
#Environment = "Production"
Environment = "Test"

def get_ip():
    if Environment == "Test":
        print "Running on Test Environment..."
        return "127.0.0.1"
    elif Environment == "Production":
        print "Running on Production Environment..."
        return "135.23.123.67"

def set_debug():
    if Environment == "Test":
        debug_value = True
        return debug_value
    elif Environment == "Production":
        debug_value = False
>>>>>>> fa513acae424844c0db6752cfaa472549f4c9c7b
        return debug_value
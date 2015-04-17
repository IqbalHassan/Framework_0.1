# -*- coding: cp1252 -*-
import os
import time

###########Production / Dev Config variables######################
#Environment = "Test"
Environment = "Production"
 
def get_ip(print_env=False):
    if Environment == "Test":
        if print_env:
            print "Running on Test Environment..."
        return "127.0.0.1"
    elif Environment == "Production":
        if print_env:
            print "Running on Production Environment..."
        return "135.23.123.206"

def set_debug():
    if Environment == "Test":
        debug_value = True
        return debug_value
    elif Environment == "Production":
        debug_value = False

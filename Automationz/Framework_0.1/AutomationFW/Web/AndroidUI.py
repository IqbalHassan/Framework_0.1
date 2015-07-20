__author__ = 'Raju'
import os
import subprocess
import time
from uiautomator import Device
from AutomationFW.Web.AndroidSupport import check_connection,make_call,look_for_incoming_call,receive_call,reject_call,hold_call
def main():
    d=[{
        'id':'F4AZCY05A885',
        'cell':'01719267494',
        'brand':'asus',
    },{
        'id':'4d00f8cee4d74200',
        'cell':'01721770326',
        'brand':'samsung',
    },]

    device_list=[each['id'] for each in d]
    print device_list
    if check_connection(device_list):
        make_call(d[1]['id'],d[0]['cell'])
        if look_for_incoming_call(d[0]['id'],30):
            receive_call(d[0]['id'])
        hold_call(d[1]['id'],'com.android.incallui:id/onScreenMenuBtn|id|5,Hold|text')
        #hold_call(d[0]['id'],'com.asus.asusincallui:id/holdButton|id|8')
        reject_call(d[0]['id'])
    else:
        print "Check Device USB connection"
        return False

if __name__=='__main__':
    main()
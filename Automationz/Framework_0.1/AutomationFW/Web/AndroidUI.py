__author__ = 'Raju'
import os
import subprocess
import time
from uiautomator import Device
class cell_phone():
    def __init__(self,d):
        for each in d:
            setattr(self,each,d[each])
    def rep_(self):
        return "id:%s, number:%s,brand:%s"%(self.id,self.cell,self.brand)
def make_phone_call(caller,callee):
    adb_command="adb -s %s shell am start -a android.intent.action.CALL -d tel:%s"%(caller.id,callee.cell)
    print adb_command
    os.system(adb_command)
def look_for_signal(cell,t):
    status=False
    while(t>0):
        adb_command="adb -s %s shell dumpsys telephony.registry|findstr \"mCallState\""%(cell.id)
        s=subprocess.Popen(adb_command,shell=True,stdout=subprocess.PIPE)
        p=int(s.communicate()[0].strip().split("mCallState=")[1])
        if p==0:
            print "idle"
        if p==1:
            print "ringing"
            status=True
            break
        if p==2:
            print "connected"
        time.sleep(1)
        t-=1
    return status
def receive_call(callee):
    adb_command="adb -s %s shell input keyevent 5"%(callee.id)
    print "connecting the call"
    os.system(adb_command)
def reject_call(callee):
    adb_command="adb -s %s shell input keyevent 6"%(callee.id)
    print "rejecting the call"
    os.system(adb_command)
def hold_call(callee):
    print callee.brand
    d=Device(callee.id,adb_server_host='127.0.0.1',adb_server_port=5037)
    if callee.brand=='asus':
        print "finding the button"
        d(resourceId='com.asus.asusincallui:id/holdButton').click()
        d.screenshot('incall.png')
        print "pressed the button"
    if callee.brand=='samsung':
        print "found samsung"
        d(resourceId='com.android.incallui:id/onScreenMenuBtn').click()
        print "pressed the menu button"
        #d(resourceId='com.android.incallui:id/holdButton').click()
        d(text="Hold").click()
        print "pressed the hold button"
def check_connectivity_first(devices):
    id_list=[x.id for x in devices]
    #print id_list
    adb_commnd="adb devices"
    s=subprocess.Popen(adb_commnd,shell=False,stdout=subprocess.PIPE)
    p=s.communicate()[0]
    p=p.split("List of devices attached")[1].strip().split("\r\n")
    attached_device=[]
    for each in p:
        d=each.split('\tdevice')[0].strip()
        attached_device.append(d)
    un_attached=list(set(id_list)-set(attached_device))
    if un_attached:
        print ",".join(un_attached)+' not attached by usb'
        return False
    else:
        print "All devices are attached"
        return True
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
    device_list=[]
    for each in d:
        device_list.append(cell_phone(each))
    print device_list
    for e in device_list:
        print e.rep_()
    if check_connectivity_first(device_list):
        make_phone_call(device_list[1],device_list[0])
        if(look_for_signal(device_list[0],30)):
            receive_call(device_list[0])
        time.sleep(5)
        hold_call(device_list[1])
        time.sleep(5)
        reject_call(device_list[0])
    else:
        print "Check Connectivity First"
        return False
if __name__=='__main__':
    main()
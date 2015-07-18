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
        return "id:%s, number:%s"%(self.id,self.cell)
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
    d=Device(callee.id,adb_server_host='127.0.0.1',adb_server_port=5037)
    print "finding the button"
    d(resourceId='com.asus.asusincallui:id/holdButton').click()
    d.screenshot('incall.png')
    print "pressed the button"
def main():
    d=[{
        'id':'F4AZCY05A885',
        'cell':'01719267494'
    },{
        'id':'4d00f8cee4d74200',
        'cell':'01721770326'
    },{
        'id':'',
        'cell':'01684667279'
    }]
    device_list=[]
    for each in d:
        device_list.append(cell_phone(each))

    make_phone_call(device_list[1],device_list[0])
    if(look_for_signal(device_list[0],30)):
        receive_call(device_list[0])
    time.sleep(5)
    hold_call(device_list[0])
    time.sleep(5)
    make_phone_call(device_list[0],device_list[2])
    time.sleep(5)
    reject_call(device_list[1])
if __name__=='__main__':
    main()
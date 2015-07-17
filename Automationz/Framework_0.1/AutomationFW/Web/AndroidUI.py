__author__ = 'Raju'
"""import os
import shlex,subprocess
from appium import webdriver
import requests
import time
host='127.0.0.1'
port=4732
whole_device_list=[]
class android_driver():
    def __init__(self,host,port,d):
        self.host=host
        self.port=port
        if 'deviceName' in d.keys():
            self.device_id=d['deviceName']
        if(self.start_separate_appium_server(host,port)):
            i=0
            while(i<100):
                s=self._poll()
                if s:
                    self.driver=self._setup(d)
                    print "up already"
                    break

    def _poll(self):
        up=False
        try:
            r=requests.get('http://'+str(self.host)+':'+str(self.port)+'/wd/hub')
            print r.status_code
            if r.status_code ==404:
                up=True
        except:
            print "not up"
        return up
    def _setup(self,d):
        remote_driver=webdriver.Remote('http://'+str(self.host)+':'+str(self.port)+'/wd/hub',d)
        return remote_driver
    def start_separate_appium_server(self,host,port):
        total_path=['Appium','node_modules','appium','bin','Appium.js']
        base_=os.environ['PROGRAMFILES']
        for each in total_path:
            base_=os.path.join(base_,each)
        base_=base_.replace("\\",'/')
        total_command='node "'+base_+'" -p '+str(port)+' -a '+str(host)
        os.system('start cmd /k '+total_command)
        return True
    def phone_call(self,number):
        txt_btn=self.driver.find_element_by_id('com.dexetra.dialer:id/txt_login_skip_signin')
        txt_btn.click()
        done_btn=self.driver.find_element_by_id('android:id/button3')
        done_btn.click()
        dialup_but=self.driver.find_element_by_id('com.dexetra.dialer:id/button_dialpad')
        dialup_but.click()
        edt_txt=self.driver.find_element_by_id('com.dexetra.dialer:id/digits')
        edt_txt.send_keys(number)
        submit_bt=self.driver.find_element_by_id('com.dexetra.dialer:id/dialButton')
        submit_bt.click()
    def cut_call(self):
        self.driver.find_element_by_id('com.android.incallui:id/endButton').click()

    def make_and_cut_call(self,number):
        self.phone_call(number)
        self.cut_call()
    def check_for_phone_call(self,time):
        while(time>0):
            print "decreasing"
            time.sleep(1)
            time-=1
        return 0
    def shell(self,cmd):
        total_command="adb -s "+self.device_id+" shell "+cmd.strip()
        os.system(total_command)
def main():
    device_1={
    'platformName':'Android',
    'platformVersion':'4.2',
    'deviceName': 'F4AZCY05A885',
    'udid':'F4AZCY05A885' ,
    'app':'E:\Workspace\\android\DialApp_2.8_35.apk',
    'newCommandTimeout':'3600'
    }
    device_2={
        'platformName':'Android',
        'platformVersion':'4.2',
        'deviceName': '4d00f8cee4d74200',
        'udid':'4d00f8cee4d74200' ,
        'app':'E:\Workspace\\android\DialApp_2.8_35.apk',
        'newCommandTimeout':'3600'
    }
    devices=[device_1,device_2]
    host='127.0.0.1'
    start_port=4729
    setup_device(devices,host,start_port)
    caller=whole_device_list[0]
    callee=whole_device_list[1]
    callee.phone_call('01719267494')
    time.sleep(7)
    caller.shell('dumpsys telephony.registry|findstr "mCallState"')
    callee.cut_call()
    os.system('taskkill /f /IM node.exe')
    os.system('taskkill /f /IM cmd.exe')

def setup_device(devices,host,start_port):
    for each in devices:
        whole_device_list.append(android_driver(host,start_port,each))
        start_port+=1

if __name__=='__main__':
    main()
"""
import os
import subprocess
import time
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
def main():
    d=[{
        'id':'F4AZCY05A885',
        'cell':'01719267494'
    },{
        'id':'4d00f8cee4d74200',
        'cell':'01721770326'
    }]
    device_list=[]
    for each in d:
        device_list.append(cell_phone(each))

    make_phone_call(device_list[1],device_list[0])
    if(look_for_signal(device_list[0],30)):
        receive_call(device_list[0])
if __name__=='__main__':
    main()
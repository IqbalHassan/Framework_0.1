__author__ = 'Raju'
import inspect,os,sys,subprocess,time
from AutomationFW.CoreFrameWork import CommonUtil
from uiautomator import Device
from AutomationFW.CoreFrameWork import Global
local_run=True
def make_call(caller_id,number):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo,"Trying to make a call from device %s to number %s"%(caller_id,number),1,local_run)
    call_command="adb -s %s shell am start -a android.intent.action.CALL -d tel:%s"%(caller_id,number)
    os.system(call_command)
    CommonUtil.ExecLog(sModuleInfo,"Made a call successfully from device %s to number %s"%(caller_id,number))

def reject_call(caller_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo,"Trying to reject the call from device %s"%(caller_id),1,local_run)
    reject_command="adb -s %s shell input keyevent KEYCODE_ENDCALL"%(caller_id)
    os.system(reject_command)
    CommonUtil.ExecLog(sModuleInfo,"Rejected call from device %s"%(caller_id))

def receive_call(caller_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo,"Trying to receive the call from device %s"%(caller_id),1,local_run)
    accept_command="adb -s %s shell input keyevent KEYCODE_CALL"%(caller_id)
    os.system(accept_command)
    CommonUtil.ExecLog(sModuleInfo,"Received call from device %s"%(caller_id))

def look_for_incoming_call(caller_id,t):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    status=False
    while(t>0):
        check_command="adb -s %s shell dumpsys telephony.registry|findstr \"mCallState\""%(caller_id)
        s=subprocess.Popen(check_command,shell=True,stdout=subprocess.PIPE)
        p=int(s.communicate()[0].strip().split("mCallState=")[1])
        if p==1:
            print "ringing"
            status=True
            break
        time.sleep(1)
        t-=1
    return status

def check_connection(device_list):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    adb_commnd="adb devices"
    s=subprocess.Popen(adb_commnd,shell=False,stdout=subprocess.PIPE)
    p=s.communicate()[0]
    p=p.split("List of devices attached")[1].strip().split("\r\n")
    attached_device=[]
    for each in p:
        d=each.split('\tdevice')[0].strip()
        attached_device.append(d)
    un_attached=list(set(device_list)-set(attached_device))
    if un_attached:
        print ",".join(un_attached)+' not attached by usb'
        return False
    else:
        print "All devices are attached"
        return True

def click_element_by_id(device_id,id_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    d=Device(device_id,adb_server_host=Global.database_ip,adb_server_port=Global.adb_port)
    CommonUtil.ExecLog(sModuleInfo,"Clicking the element with id %s in device %s"%(id_name,device_id),1,local_run)
    d(resourceId=id_name).click()
    CommonUtil.ExecLog(sModuleInfo,"Successfully clicked the element with id %s in device %s"%(id_name,device_id),1,local_run)
    return True

def click_element_by_text(device_id,id_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    d=Device(device_id,adb_server_host=Global.database_ip,adb_server_port=Global.adb_port)
    CommonUtil.ExecLog(sModuleInfo,"Clicking the element with text %s in device %s"%(id_name,device_id),1,local_run)
    d(text=id_name).click()
    CommonUtil.ExecLog(sModuleInfo,"Successfully clicked the element with text %s in device %s"%(id_name,device_id),1,local_run)
    return True

def hold_call(device_id,tap_sequence):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    default_time=2
    tap_sequence=tap_sequence.split(",")
    for each in tap_sequence:
        listing=each.split("|")
        if len(listing)==2:
            id_name=listing[0]
            tag_name=listing[1]
            time_out=default_time
        elif len(listing)>2:
            id_name=listing[0]
            tag_name=listing[1]
            if listing[2]!='':
                time_out=listing[2]
            else:
                time_out=default_time
        else:
            CommonUtil.ExecLog(sModuleInfo,"Invalid format in tap sequence",3,local_run)
            return False
        print id_name,tag_name,time_out
        if tag_name=='id':
            click_element_by_id(device_id,id_name)
        if tag_name=='text':
            click_element_by_text(device_id,id_name)
        time.sleep(int(time_out))
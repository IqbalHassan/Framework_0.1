__author__ = 'Raju'
from appium import webdriver
import os,sys
import inspect
from AutomationFW.CoreFrameWork import CommonUtil
from AutomationFW.Web import AndroidSupport
def open_app(dependency,step_data,temp_q):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        app_name=step_data[0][0][1]
        sTestStepReturnStatus = AndroidSupport.init(app_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

def open_activity(dependency,step_data,temp_q):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        activity_name=step_data[0][0][1]
        package_name=step_data[0][1][1]
        sTestStepReturnStatus = AndroidSupport.openActivity(package_name,activity_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

def sign_in(dependency,step_data,temp_q):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        username=step_data[0][0][1]
        password=step_data[0][1][1]
        sTestStepReturnStatus = AndroidSupport.login(username,password)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def close_app(dependency,step_data,temp_q):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sTestStepReturnStatus = AndroidSupport.close()
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

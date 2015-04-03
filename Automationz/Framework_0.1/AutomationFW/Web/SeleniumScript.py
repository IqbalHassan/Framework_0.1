
import sys
import os
sys.path.append("..")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#Ver1.0
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from CoreFrameWork import CommonUtil
from selenium.webdriver.support import expected_conditions as EC

global WebDriver_Wait 
WebDriver_Wait = 60

#if local_run is True, no logging will be recorded to the web server.  Only local print will be displayed
#local_run = True
local_run = False

def BrowserSelection(browser):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.close()
    except:
        True
    global sBrowser
    try:
        browser = browser.lower()
        if "chrome" in browser:
            sBrowser = webdriver.Chrome()
            sBrowser.implicitly_wait(WebDriver_Wait)
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Chrome Browser", 1, local_run)
            return "passed"
        elif browser == 'firefox':
            sBrowser = webdriver.Firefox()
            sBrowser.implicitly_wait(WebDriver_Wait)
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Firefox Browser", 1, local_run)
            return "passed"
        elif "ie" in browser:
            sBrowser = webdriver.Ie()
            sBrowser.implicitly_wait(WebDriver_Wait)
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Internet Explorer Browser", 1, local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "You did not select a valid browser: %s" % browser, 3,local_run)
            return "failed"
        #time.sleep(3)
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3,local_run)
        return "failed"

def OpenLink(link, page_title):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.get(link)
        sBrowser.implicitly_wait(WebDriver_Wait)
        CommonUtil.ExecLog(sModuleInfo, "Successfully opened your link: %s" % link, 1,local_run)
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        assert page_title in sBrowser.title
        #time.sleep(3)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "failed to open your link: %s. Error:%s" %(link, Error_Detail), 3,local_run)
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        return "failed"

def Login(user_name,password,logged_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        Click_Element_By_Name("Log in")
        Set_Text_Field_Value_By_ID("username",user_name)
        Set_Text_Field_Value_By_ID("password",password)
        Click_Element_By_ID ("loginbtn")
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Successfully logged in", 1, local_run)
        element_login = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[@title='View profile']")))
        if (WebDriverWait(element_login, WebDriver_Wait).until(lambda driver : element_login.text)) == logged_name:
            CommonUtil.ExecLog(sModuleInfo, "Verified that logged in as: %s"%logged_name, 1,local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Log in failed for user: %s"%logged_name, 3,local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to login.  %s"%Error_Detail, 3,local_run)
        return "failed"
    
def Expand_Menu_By_ID(_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_id, 1,local_run)
        try: 
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.ID, _id)))
            CommonUtil.ExecLog(sModuleInfo, "Found your element by ID: %s"%_id, 1,local_run)
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by ID: %s"%_id, 3,local_run)
            return "failed"
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        #parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        parent = WebDriverWait(Element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        #grand_parent = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath(".."))
        grand_parent = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if expand_status == 'true':
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%_id, 2,local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%_id, 1,local_run)
            sBrowser.implicitly_wait(WebDriver_Wait)
            Element.click()  
        #Verify if it was expanded 
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if (expand_status== "true"):
            CommonUtil.TakeScreenShot(sModuleInfo, local_run)
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%_id, 1,local_run)
            #time.sleep(3)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%_id, 3,local_run)
            return "failed"   
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.  Error: %s"%(_id, Error_Detail), 3,local_run)
        return "failed"    

    
def Expand_Menu_By_Name(_name,parent=False):
    '''
    Use this only if you are confident that there wont be any duplicate item with same name
    Otherwise, use Expand_Menu_By_ID
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_name, 1,local_run)
        if isinstance(parent, (bool)) == True:
            #allElements = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_elements_by_xpath("//*[text()='%s']"%_name)) 
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='%s']"%_name)))
        else:
            #allElements = parent.find_elements_by_xpath("//*[text()='%s']"%_name)
            Element = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='%s']"%_name)))
            #allElements = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_elements_by_xpath("//*[text()='%s']"%_name)) 
        
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        #parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        #grand_parent = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath(".."))
        sBrowser.implicitly_wait(WebDriver_Wait)
        parent = WebDriverWait(Element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        grand_parent = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if expand_status == 'true':
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%_name, 2, local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%_name, 1,local_run)
            wait = WebDriverWait(sBrowser, 10)
            Element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='%s']"%_name)))
            Element.click()
        #Verify if it was expanded 
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if (expand_status== "true"):
            CommonUtil.TakeScreenShot(sModuleInfo, local_run)
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%_name, 1,local_run)
            #time.sleep(3)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%_name, 3,local_run)
            return "failed"   
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.  Error: %s"%(_name, Error_Detail), 3,local_run)
        return "failed"    

def Click_Element_By_Name(_name,parent=False):
    '''
    Use this function only if you are sure that there wont be any conflicting Name.
    If possible use Click_Element_By_ID
    
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_name, 1,local_run)
        if isinstance(parent, (bool)) == True:
            allElements = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()='%s']"%_name)))        
        else:
            allElements = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()='%s']"%_name)))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%_name, 3,local_run)
            return "failed"
        else:
            if len(allElements) > 1:
                CommonUtil.ExecLog(sModuleInfo, "Found more than one element and will use the first one.  ** if fails, try providing parent element or try by ID** ", 2, local_run)
            for each in allElements:
                if (WebDriverWait(each, WebDriver_Wait).until(lambda driver : each.is_displayed())) == True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%_name, 1,local_run)
                    break   
        #Now we simply click it
        Element.click()
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%_name, 1,local_run)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.   Error: %s"%(_name,Error_Detail), 3,local_run)
        return "failed"    
 

def Click_Element_By_ID(_id):    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%_id, 1,local_run)
        try:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.ID, _id)))
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%_id, 3,local_run)
            return "failed"
        #Now we simply click it
        Element.click()
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%_id, 1,local_run)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to click element by ID: %s.  Error: %s"%(_id,Error_Detail), 3,local_run)
        return "failed"    


def Set_Text_Field_Value_By_ID(_id,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by id: %s"%_id, 1,local_run)
        try:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.ID, _id)))
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by ID: %s"%_id, 3,local_run)
            return "failed"  
        #Now we simply click it
        Element.click()
        Element.clear()
        Element.send_keys(value)
        Element.click()
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Successfully set the value of to text with ID: %s"%_id, 1,local_run)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value for your ID: %s.  Error: %s"%(_id, Error_Detail), 3,local_run)
        return "failed"    

def Click_Element_By_Custome_Field_Value(field,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by field: %s and value: %s"%(field,value), 1,local_run)
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//input[@%s='%s']"%(field,value))))
        #Now we simply click it
        Element.click()
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element by field: %s and value: %s"%(field,value), 1,local_run)
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to click your element by field: %s and value: %s.  Error: %s"%(field,value, Error_Detail), 3,local_run)
        return "failed"    

def Verify_Text_Message_By_Class(element, expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1, local_run)
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME, "message")))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == expected_text:
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1,local_run)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1,local_run)
            return "passed"            
        else:
            CommonUtil.ExecLog(sModuleInfo, "failed to verify your expected text: %s"%expected_text, 3,local_run)
            CommonUtil.ExecLog(sModuleInfo, "Expected text was:'%s' but Actual text was '%s' "%(expected_text,actual_text), 3,local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Error occur during verification process.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"  

def Course_Exists(course):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Searching for course: %s"%course, 1,local_run)
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'%s')]" %course)))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == course:
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified that course exists: %s"%actual_text, 1,local_run)
            return "passed"            
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find your course: %s.  Error: %s"%(course,Error_Detail), 3,local_run)
        return "failed"  

def Verify_Text_Message_By_Text(expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1, local_run)
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'%s')]" %expected_text)))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == expected_text:
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1,local_run)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1,local_run)
            return "passed"            
        else:
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 3,local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Could not find your expected text: %s. Error: %s"%(expected_text, Error_Detail), 3,local_run)
        return "failed"  

def Course_Settings_Time_Limit(completion_time_id, completion_time_value,daily_time_id, daily_time_value,submit_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Entering completion time in minutes", 1, local_run)
        result = Set_Text_Field_Value_By_ID(completion_time_id,completion_time_value)
        if result == "failed":
            CommonUtil.ExecLog(sModuleInfo, "failed to entered the completion time value", 3, local_run)
            CommonUtil.TakeScreenShot(sModuleInfo, local_run)
            return "failed"
        else: 
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the completion time value", 1, local_run)
        #----------------
        CommonUtil.ExecLog(sModuleInfo, "Entering daily time limit", 1, local_run)
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        result = Set_Text_Field_Value_By_ID(daily_time_id,daily_time_value)
        if result == "failed":
            CommonUtil.ExecLog(sModuleInfo, "failed to entered the daily time limit", 3, local_run)
            CommonUtil.TakeScreenShot(sModuleInfo, local_run) 
            return "failed"
        else: 
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the daily time limit", 1, local_run)
        #----------------
        #Save Configuration 
        CommonUtil.ExecLog(sModuleInfo, "Clicking Save Config button", 1,local_run)
        Click_Element_By_ID(completion_time_id)
        result = Click_Element_By_ID(submit_id) 
        if result == "failed":
            CommonUtil.ExecLog(sModuleInfo, "failed to click on Save Config button", 3, local_run)
            return "failed"
        else: 
            CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1, local_run)
        CommonUtil.TakeScreenShot(sModuleInfo, local_run) 
        #time.sleep(3)
        return "passed"      
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value course settings information.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"  

def Turn_Editing_On_OR_Off(on_off):
    '''
    This function expects the word "on" or "off".  
    If editing is already turned on and you are trying to turn it on again, 
    it will not fail and return as warning.
    Example:
        To turn editing on: Turn_Editing_On_OR_off('on')
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name   
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        if on_off == "on":
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing is Turned On or Off", 1, local_run)
            result = Expand_Menu_By_Name('Front page settings')
            if result == "failed":
                CommonUtil.ExecLog(sModuleInfo, "Unable to find the menu Front Page settings.", 3, local_run)
                return "failed"
            expected_text = 'Turn editing'
            try:
                Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'%s')]" %expected_text)))
            except Exception, e:
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3, local_run)
                return "failed"
            if (WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)) ==  'Turn editing off':
                CommonUtil.ExecLog(sModuleInfo, "Editing is already on", 1, local_run)
                time.sleep(5)
                return "passed"
            else:
                CommonUtil.ExecLog(sModuleInfo, "Turning Editing on", 1, local_run)
                result = Click_Element_By_Name('Turn editing on')
                if result == "failed":
                    CommonUtil.ExecLog(sModuleInfo, "Failed to turn Editing on", 3, local_run)
                    return "failed"
                else:
                    CommonUtil.ExecLog(sModuleInfo, "Successfully turned Editing on", 1, local_run)
                    time.sleep(5)
                    return "passed"
        elif on_off == "off":
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing is Turned On or Off", 1, local_run)
            Expand_Menu_By_Name('Front page settings')
            expected_text = 'Turn editing'
            try:
                Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'%s')]" %expected_text)))
            except Exception, e:
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3, local_run)
                return "failed"
            if ((WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text))) ==  'Turn editing on':
                CommonUtil.ExecLog(sModuleInfo, "Editing is already off", 1, local_run)
                time.sleep(5)
                return "passed"
            else:
                CommonUtil.ExecLog(sModuleInfo, "Turning Editing on", 1, local_run)
                result = Click_Element_By_Name('Turn editing off')              
                if result == "failed":
                    CommonUtil.ExecLog(sModuleInfo, "Failed to turn Editing on", 3, local_run)
                    return "failed"
                else:
                    time.sleep(5)
                    CommonUtil.ExecLog(sModuleInfo, "Successfully turned Editing on", 1, local_run)
                    return "passed"        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "We are unable to control the editing option.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"
        
    
def Click_By_Parameter_And_Value(parameter,value, parent=False):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Locating your element...", 1, local_run)
        if isinstance(parent, (bool)) == True:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[@%s='%s']"%(parameter,value))))
        else:
            Element = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[@%s='%s']"%(parameter,value))))
        CommonUtil.ExecLog(sModuleInfo, "Found element and clicking..", 1, local_run)
        Element.click()
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked by %s and %s"%(parameter,value), 1,local_run)
        return "passed" 
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to locate element to click.  Parameter: %s & Value: %s  Error: %s"%(parameter,value,Error_Detail), 3,local_run)
        return "failed"
    
def ClickSafety_Course_Settings(): 
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        result = Expand_Menu_By_Name('Site administration')
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3, local_run)
            return "failed"        
        #Since below are all under Site Admin, we should restrict our search within Site admin.
        #admin_tab = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath("//*[text()='Site administration']"))
        admin_tab = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Site administration']")))
        #sibling = WebDriverWait(admin_tab, WebDriver_Wait).until(lambda driver :admin_tab.find_element_by_xpath(".."))
        #parent = WebDriverWait(sibling, WebDriver_Wait).until(lambda driver :sibling.find_element_by_xpath(".."))
        sibling = WebDriverWait(admin_tab, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        parent = WebDriverWait(sibling, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        result = Expand_Menu_By_Name('Plugins',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3, local_run)
            return "failed" 
        result = Expand_Menu_By_Name('Local plugins',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3, local_run)
            return "failed" 
        result = Expand_Menu_By_Name('ClickSafety',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3, local_run)
            return "failed"        
        result = Click_Element_By_Name('Course settings',parent) 
        if result == "passed":
            CommonUtil.ExecLog(sModuleInfo, "Click course settings for ClickSafety menu", 1, local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3, local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"    

def Edit_Course_From_Course_Settings(course_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #First we need to find the main table.  From there we will look for course name
        CommonUtil.ExecLog(sModuleInfo, "Locating Course Settings table..", 1, local_run)
        #table_ = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_id("region-main"))
        table_ = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.ID, "region-main")))
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        CommonUtil.ExecLog(sModuleInfo, "Locating your course name...", 1, local_run)
        #allElements = WebDriverWait(table_, WebDriver_Wait).until(lambda driver :table_.find_elements_by_xpath("//*[text()='%s']"%course_name))
        allElements = WebDriverWait(table_, WebDriver_Wait).until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()='%s']"%course_name)))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%course_name, 3,local_run)
            return "failed"
        else:
            if len(allElements) > 1:
                CommonUtil.ExecLog(sModuleInfo, "Found more than one element and will use the first one.  ** if fails, try to locate the element manually ** ", 2, local_run)
            for each in allElements:
                if (WebDriverWait(each, WebDriver_Wait).until(lambda driver : each.is_displayed())) == True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your course by name: %s.  Using the first element found to click"%course_name, 1,local_run)                  
                    break
        #We need to go one up so we can locate the row ID.  From there we will be able to find the children element for EDIT
        #parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        parent = WebDriverWait(Element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        #Edit_Button = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath("//*[@title='Edit']"))
        Edit_Button = WebDriverWait(parent, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Edit']")))
        Edit_Button.click()
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Edit button for the course: %s"%course_name, 1,local_run)
        return "passed"                              
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to Edit your course: %s.  Error: %s"%(course_name,Error_Detail), 3,local_run)
        return "failed"    

def Tear_Down():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot(sModuleInfo, local_run)
        sBrowser.close()
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1, local_run)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"

def Delete_A_Course(course_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        Expand_Menu_By_Name('Site administration')
        time.sleep(3)
        CommonUtil.ExecLog(sModuleInfo, "Find site admin top level element", 1, local_run)
        site_admin_element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Site administration']")))
        parent_site_admin = WebDriverWait(site_admin_element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        grand_parent_site_admin = WebDriverWait(parent_site_admin, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))        
        CommonUtil.ExecLog(sModuleInfo, "Expand Courses from site admin menu", 1, local_run)
        Expand_Menu_By_Name("Courses",grand_parent_site_admin)
        CommonUtil.ExecLog(sModuleInfo, "Manage courses and categories", 1, local_run)
        Click_Element_By_Name('Manage courses and categories',grand_parent_site_admin)
        CommonUtil.ExecLog(sModuleInfo, "Search for course: %s"%course_name, 1,local_run)        
        Set_Text_Field_Value_By_ID('coursesearchbox',course_name)
        Click_By_Parameter_And_Value("value","Go")
        time.sleep(5)
        CommonUtil.ExecLog(sModuleInfo, "Waiting for search result page to show up", 1, local_run)          
        search_course_list = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-listing')))
        CommonUtil.ExecLog(sModuleInfo, "Searching for course: %s"%course_name, 1,local_run)  
        try:
            course_element = WebDriverWait(search_course_list, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='%s']"%course_name)))    
            CommonUtil.ExecLog(sModuleInfo, "Found your course: %s"%course_name, 1,local_run)
        except:
            CommonUtil.ExecLog(sModuleInfo, "Unable to find your course.  Make sure course exists", 3, local_run)
            return "failed"
        CommonUtil.ExecLog(sModuleInfo, "Deleting your course: %s"%course_name, 1,local_run)
        course_element_row = WebDriverWait(course_element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        Click_By_Parameter_And_Value("alt","Delete",course_element_row)
        time.sleep(5)
        Click_By_Parameter_And_Value ("value","Continue")
        CommonUtil.ExecLog(sModuleInfo, "Successfully deleted your course: %s"%course_name, 1,local_run)
        CommonUtil.ExecLog(sModuleInfo, "Verifying if course is deleted completely", 1, local_run)
        delete_result =  Verify_Text_Message_By_Text('%s has been completely deleted'%course_name)
        if delete_result == "passed":
            CommonUtil.ExecLog(sModuleInfo, "Completely deleted your course: %s"%course_name, 1,local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Could not verify if course was deleted completely", 3, local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to create course.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"

def Create_A_New_Course(course_name, short_name, course_id, cleanup=True):
    '''
    it assumes that you are logged in as Admin
    Editing is on
    This function accepts: 
    course_name =  name of the course. 
    cleanup = true if you want to delete old name or false if you want to just keep the name if it already there
    '''
    """
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        Click_Element_By_Name('Home')
        course_exists = Course_Exists(course_name)
        if (course_exists == "passed") and (cleanup=='true'):
            print "Existing course found and will be deleted"
            result = Delete_A_Course(course_name)
            if result == "failed":
                print "Unable to delete an existing course"
                return "failed"
        elif (course_exists == "passed") and (cleanup!='true'):
            print "Course already exists and clean up was set not to re-create"
            return "passed"
        else:
            print "Course name was not found and will be created"
        Turn_Editing_On_OR_Off("on")
        Expand_Menu_By_Name('Site administration')
        Expand_Menu_By_ID('yui_3_15_0_3_1424235876713_5248')
        Click_Element_By_Name('Manage courses and categories')
        Click_Element_By_Name('Miscellaneous')
        Click_Element_By_Name('Create new course')
        Set_Text_Field_Value_By_ID('id_fullname',course_name)
        Set_Text_Field_Value_By_ID('id_shortname',short_name)
        Set_Text_Field_Value_By_ID('id_idnumber',course_id)
        Click_By_Parameter_And_Value("value","Save changes")
        course_name_verify = "%s: 0 enrolled users"%course_name
        Verify_Text_Message_By_Text(course_name_verify)
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to create course.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"
    """
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        Expand_Menu_By_Name('Site administration')
        time.sleep(3)
        CommonUtil.ExecLog(sModuleInfo, "Find site admin top level element", 1, local_run)
        site_admin_element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Site administration']")))
        parent_site_admin = WebDriverWait(site_admin_element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
        grand_parent_site_admin = WebDriverWait(parent_site_admin, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))        
        CommonUtil.ExecLog(sModuleInfo, "Expand Courses from site admin menu", 1, local_run)
        Expand_Menu_By_Name("Courses",grand_parent_site_admin)
        CommonUtil.ExecLog(sModuleInfo, "Manage courses and categories", 1, local_run)
        Click_Element_By_Name('Manage courses and categories',grand_parent_site_admin)
        CommonUtil.ExecLog(sModuleInfo, "Search for course: %s"%course_name, 1,local_run)        
        Set_Text_Field_Value_By_ID('coursesearchbox',course_name)
        Click_By_Parameter_And_Value("value","Go")
        time.sleep(5)
        CommonUtil.ExecLog(sModuleInfo, "Waiting for search result page to show up", 1, local_run)          
        search_course_list = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-listing')))
        CommonUtil.ExecLog(sModuleInfo, "Searching for course: %s"%course_name, 1,local_run)  
        try:
            course_element = WebDriverWait(search_course_list, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[text()='%s']"%course_name)))    
            CommonUtil.ExecLog(sModuleInfo, "Found your course: %s"%course_name, 3,local_run)
            if isinstance(cleanup, bool) and cleanup:
                CommonUtil.ExecLog(sModuleInfo, "Deleting your course: %s"%course_name, 1,local_run)
                course_element_row = WebDriverWait(course_element, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "..")))
                Click_By_Parameter_And_Value("alt","Delete",course_element_row)
                time.sleep(5)
                Click_By_Parameter_And_Value ("value","Continue")
                CommonUtil.ExecLog(sModuleInfo, "Successfully deleted your course: %s"%course_name, 1,local_run)
                CommonUtil.ExecLog(sModuleInfo, "Verifying if course is deleted completely", 1, local_run)
                delete_result =  Verify_Text_Message_By_Text('%s has been completely deleted'%short_name)
                if delete_result == "passed":
                    CommonUtil.ExecLog(sModuleInfo, "Completely deleted your course: %s"%course_name, 1,local_run)
                else:
                    CommonUtil.ExecLog(sModuleInfo, "Could not verify if course was deleted completely", 3, local_run)
                    return "failed"
            else:
                CommonUtil.ExecLog(sModuleInfo, "Found the course but no delete is requested", 1,local_run)
                return "failed"
        except:
            CommonUtil.ExecLog(sModuleInfo, "Unable to find your course.", 1, local_run)
        print "Create you course now"
        CommonUtil.ExecLog(sModuleInfo, "Clicking Manage Course and Categories", 1, local_run)
        Click_By_Parameter_And_Value("class","tree_item leaf active_tree_node")
        CommonUtil.ExecLog(sModuleInfo, "Clicking Miscellaneous", 1, local_run)
        miscellaneous_admin_element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME,'ml')))
        Click_Element_By_Name('Miscellaneous',miscellaneous_admin_element)
        CommonUtil.ExecLog(sModuleInfo, "Clicking New Course Button", 1, local_run)
        course_parent_element=WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME,'course-listing-actions')))
        Click_Element_By_Name("Create new course", course_parent_element)
        CommonUtil.ExecLog(sModuleInfo, "Entering Course Full Name", 1, local_run)
        Set_Text_Field_Value_By_ID('id_fullname',course_name)
        CommonUtil.ExecLog(sModuleInfo, "Entering Course Short Name", 1, local_run)
        Set_Text_Field_Value_By_ID('id_shortname',short_name)
        CommonUtil.ExecLog(sModuleInfo, "Entering Course ID", 1, local_run)
        Set_Text_Field_Value_By_ID('id_idnumber',course_id)        
        CommonUtil.ExecLog(sModuleInfo, "Clicking Save Changes Button", 1, local_run)
        submit_button=WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.ID,'id_submitbutton')))
        submit_button.click()
        #checking if its' created successfully
        create_result =  WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.CLASS_NAME,'homelink')))
        if create_result.text == short_name:
            CommonUtil.ExecLog(sModuleInfo, "Successfully created your course: %s"%course_name, 1,local_run)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Could not verify if course was created successfully", 3, local_run)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable to create course.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"
        


def Verify_User_Level_Settings(user_level):    
    '''
    it assumes user is logged in
    checks to see if turn editing on/off option is there
    for admin, it expects it and for students, it does not

    '''
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        #Admin verification
        if user_level == "admin":
            CommonUtil.ExecLog(sModuleInfo, "Expanding Front Page Settings", 1, local_run)
            result = Expand_Menu_By_Name('Front page settings')
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing option is present", 1, local_run)
            if result == "failed":
                CommonUtil.ExecLog(sModuleInfo, "Unable to find the menu Front Page settings.", 1, local_run)
                CommonUtil.ExecLog(sModuleInfo, "No option was found to Turn Editing on/off.  USer is not admin", 3, local_run)
                return "failed"
            expected_text = 'Turn editing'
            try:
                Element = WebDriverWait(sBrowser, WebDriver_Wait).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'%s')]" %expected_text)))
                CommonUtil.ExecLog(sModuleInfo, "Found Editing option.  User has admin rights", 1, local_run)
                return "passed"
            except Exception, e:
                CommonUtil.ExecLog(sModuleInfo, "No option was found to Turn Editing on/off.  USer is not admin", 3, local_run)
                return "failed"
        #Student verification
        elif user_level == "student":
            CommonUtil.ExecLog(sModuleInfo, "Expanding Front Page Settings", 1, local_run)
            result = Expand_Menu_By_Name('Front page settings')
            if result == "failed":
                CommonUtil.ExecLog(sModuleInfo, "No option for Front Page Settings.  User is student", 1, local_run)
                return "Passed"
            else:
                CommonUtil.ExecLog(sModuleInfo, "Students should not have Front Page Settings", 3, local_run)
                return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        CommonUtil.ExecLog(sModuleInfo, "Unable confirm type of user.  Error: %s"%Error_Detail, 3,local_run)
        return "failed"



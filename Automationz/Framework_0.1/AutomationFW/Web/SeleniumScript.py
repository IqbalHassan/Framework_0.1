
import sys
import os
sys.path.append("..")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.selenium as Sal
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
#Ver1.0
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from CoreFrameWork import CommonUtil

global WebDriver_Wait 
WebDriver_Wait = 90

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
            print "Started Chrome Browser"
            CommonUtil.ExecLog(sModuleInfo, "Started Chrome Browser", 1)
            return "passed"
        elif browser == 'firefox':
            sBrowser = webdriver.Firefox()
            sBrowser.implicitly_wait(WebDriver_Wait)
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Firefox Browser", 1)
            print "Started Firefox Browser"
            return "passed"
        elif "ie" in browser:
            sBrowser = webdriver.Ie()
            sBrowser.implicitly_wait(WebDriver_Wait)
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Internet Explorer Browser", 1)
            print "Started Internet Explorer Browser"
            return "passed"
        else:
            print "You did not select a valid browser: %s" % browser
            CommonUtil.ExecLog(sModuleInfo, "You did not select a valid browser: %s" % browser, 3)
            return "failed"
        #time.sleep(3)
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        print "Unable to start WebDriver"
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver. %s"%Error_Detail, 3)
        return "failed"

def OpenLink(link, page_title):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.get(link)
        sBrowser.implicitly_wait(WebDriver_Wait)
        CommonUtil.ExecLog(sModuleInfo, "Successfully opened your link: %s" % link, 1)
        print "Successfully opened your link: " + link
        CommonUtil.TakeScreenShot("sModuleInfo")
        assert page_title in sBrowser.title
        #time.sleep(3)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "failed to open your link: %s. Error:%s" %(link, Error_Detail), 3)
        print "failed to open your link: %s" % link
        CommonUtil.TakeScreenShot("sModuleInfo")
        return "failed"

def Login(user_name,password,logged_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        Click_Element_By_Name("Log in")
        Set_Text_Field_Value_By_ID("username",user_name)
        Set_Text_Field_Value_By_ID("password",password)
        Click_Element_By_ID ("loginbtn")
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully logged in", 1)
        element_login =  WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_element_by_xpath("//*[@title='View profile']"))
        if (WebDriverWait(element_login, WebDriver_Wait).until(lambda driver : element_login.text)) == logged_name:
            CommonUtil.ExecLog(sModuleInfo, "Verified that logged in as: %s"%logged_name, 1)
            print "Verified that logged in as: %s"%logged_name
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Log in failed for user: %s"%logged_name, 3)
            print "Unable to login"
            return "failed"
            
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to login.  %s"%Error_Detail, 3)
        print "Unable to login"
        return "failed"
    
def Expand_Menu_By_ID(_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_id, 1)
        print "Trying to find element by ID: %s"%_id
        try: 
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_element_by_id(_id))
            CommonUtil.ExecLog(sModuleInfo, "Found your element by ID: %s"%_id, 1)
            print "Found your element by ID: %s"%_id
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by ID: %s"%_id, 3)
            print "Could not find your element by ID: %s"%_id
            return "failed"
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        grand_parent = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath(".."))
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if expand_status == 'true':
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%_id, 2)
            print "%s is already expanded "%_id
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%_id, 1)
            sBrowser.implicitly_wait(WebDriver_Wait)
            Element.click()  
        #Verify if it was expanded 
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if (expand_status== "true"):
            CommonUtil.TakeScreenShot("sModuleInfo")
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%_id, 1)
            #time.sleep(3)
            print "Successfully expanded your menu: %s"%_id
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%_id, 3)
            print "Unable to expand Menu: %s"%_id
            return "failed"   
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.  Error: %s"%(_id, Error_Detail), 3)
        print "Unable to expand Menu: %s"%_id
        return "failed"    

    
def Expand_Menu_By_Name(_name,parent=False):
    '''
    Use this only if you are confident that there wont be any duplicate item with same name
    Otherwise, use Expand_Menu_By_ID
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_name, 1)
        print "Trying to find element by name: %s"%_name
        if isinstance(parent, (bool)) == True:
            #allElements = sBrowser.find_elements_by_xpath("//*[text()='%s']"%_name)
            allElements = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_elements_by_xpath("//*[text()='%s']"%_name))
        else:
            #allElements = parent.find_elements_by_xpath("//*[text()='%s']"%_name)
            allElements = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_elements_by_xpath("//*[text()='%s']"%_name)) 
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%_name, 3)
            print "Could not find your element by name: %s"%_name
            return "failed"
        #Now find the ones that are being displayed
        else:
            if len(allElements) > 1:
                CommonUtil.ExecLog(sModuleInfo, "Found more than one element and will use the first one.  ** if fails, try providing parent element or use ID ** ", 2)
                print "Found more than one element and will use the first one.  ** if fails, try providing parent element or use ID ** "
            for each in allElements:
                if (WebDriverWait(each, WebDriver_Wait).until(lambda driver : each.is_displayed())) == True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%_name, 1)
                    print "Found your element by name: %s.  Using the first element found to click"%_name                   
                    break
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        grand_parent = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath(".."))
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if expand_status == 'true':
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%_name, 2)
            print "%s is already expanded "%_name
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%_name, 1)
            Element.click()
        #Verify if it was expanded 
        expand_status = WebDriverWait(grand_parent, WebDriver_Wait).until(lambda driver : grand_parent.get_attribute("aria-expanded"))
        expand_status = str(expand_status).lower()
        if (expand_status== "true"):
            CommonUtil.TakeScreenShot("sModuleInfo")
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%_name, 1)
            #time.sleep(3)
            print "Successfully expanded your menu: %s"%_name
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%_name, 3)
            print "Unable to expand Menu: %s"%_name
            return "failed"   
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.  Error: %s"%(_name, Error_Detail), 3)
        print "Unable to expand Menu: %s"%_name
        return "failed"    



def Click_Element_By_Name(_name,parent=False):
    '''
    Use this function only if you are sure that there wont be any conflicting Name.
    If possible use Click_Element_By_ID
    
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%_name, 1)
        print "Trying to find element by name: %s"%_name
        if isinstance(parent, (bool)) == True:
            allElements = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_elements_by_xpath("//*[text()='%s']"%_name))
        else:
            allElements = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_elements_by_xpath("//*[text()='%s']"%_name))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%_name, 3)
            print "Could not find your element by name: %s"%_name
            return "failed"
        else:
            if len(allElements) > 1:
                CommonUtil.ExecLog(sModuleInfo, "Found more than one element and will use the first one.  ** if fails, try providing parent element or try by ID** ", 2)
                print "Found more than one element and will use the first one.  ** if fails, try providing parent element or try by ID** "
            for each in allElements:
                if (WebDriverWait(each, WebDriver_Wait).until(lambda driver : each.is_displayed())) == True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%_name, 1)
                    print "Found your element by name: %s.  Using the first element found to click"%_name                   
                    break   
        #Now we simply click it
        Element.click()
        print "Successfully clicked your element by name: %s"%_name
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%_name, 1)
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s.   Error: %s"%(_name,Error_Detail), 3)
        print "Unable to expand Menu: %s"%_name
        return "failed"    
 


def Click_Element_By_ID(_id):
    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%_id, 1)
        print "Trying to find element by ID: %s"%_id
        try:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_element_by_id(_id))
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%_id, 3)
            print "Could not find your element by ID: %s"%_id
            return "failed"
        #Now we simply click it
        Element.click()
        print "Successfully clicked your element by ID: %s"%_id
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%_id, 1)
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to click element by ID: %s.  Error: %s"%(_id,Error_Detail), 3)
        print "Unable to click your element by ID: %s"%_id
        return "failed"    


def Set_Text_Field_Value_By_ID(_id,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by id: %s"%_id, 1)
        print "Trying to find element by id: %s"%_id
        try:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_element_by_id(_id))
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by ID: %s"%id, 3)
            print "Could not find your element by ID: %s"%_id
            return "failed"  
        #Now we simply click it
        Element.click()
        Element.clear()
        Element.send_keys(value)
        Element.click()
        print "Successfully set the value of to text with ID: %s"%id
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully set the value of to text with ID: %s"%id, 1)
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value for your ID: %s.  Error: %s"%(id, Error_Detail), 3)
        print "Unable to set value for your ID: %s"%id
        return "failed"    

def Click_Element_By_Custome_Field_Value(field,value):
    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by field: %s and value: %s"%(field,value), 1)
        print "Trying to find element by field: %s and value: %s"%(field,value)
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver : sBrowser.find_element_by_xpath("//input[@%s='%s']"%(field,value)))
        #Now we simply click it
        Element.click()
        print "Successfully clicked your element by field: %s and value: %s"%(field,value)
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element by field: %s and value: %s"%(field,value), 1)
        return "passed"

    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to click your element by field: %s and value: %s.  Error: %s"%(field,value, Error_Detail), 3)
        print "Unable to click your element by field: %s and value: %s"%(field,value)
        return "failed"    



def Verify_Text_Message_By_Class(element, expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1)
        print "Getting text string from the web"
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_class_name("message"))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == expected_text:
            print "Successfully verified your text: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1)
            print "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1)
            return "passed"            
        else:
            print "failed to verify your expected text: %s"%expected_text
            CommonUtil.ExecLog(sModuleInfo, "failed to verify your expected text: %s"%expected_text, 3)
            print "Expected text was:'%s' but Actual text was '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text was:'%s' but Actual text was '%s' "%(expected_text,actual_text), 3)
            return "failed"

     
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Error occur during verification process.  Error: %s"%Error_Detail, 3)
        print "Error occur during verification process"
        return "failed"  


def Course_Exists(course):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Searching for course: %s"%course, 1)
        print "Searching for course: %s"%course
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %course))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == course:
            print "Successfully verified that course exists: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified that course exists: %s"%actual_text, 1)
            return "passed"            
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Could not find your course: %s.  Error: %s"%(course,Error_Detail), 3)
        print "Could not find your expected course: %s"%course
        return "failed"  
    


def Verify_Text_Message_By_Text(expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1)
        print "Getting text string from the web"
        Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text))
        actual_text = WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)
        if actual_text == expected_text:
            print "Successfully verified your text: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1)
            print "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1)
            return "passed"            
     
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Could not find your expected text: %s. Error: %s"%(expected_text, Error_Detail), 3)
        print "Could not find your expected text: %s"%expected_text
        return "failed"  


def Course_Settings_Time_Limit(completion_time_id, completion_time_value,daily_time_id, daily_time_value,submit_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Entering completion time in minutes", 1)
        print "Entering completion time in minutes"
        result = Set_Text_Field_Value_By_ID(completion_time_id,completion_time_value)
        if result == "failed":
            print "failed to entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "failed to entered the completion time value", 3)
            CommonUtil.TakeScreenShot("sModuleInfo")
            return "failed"
        else: 
            print "Successfully entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the completion time value", 1)

        #----------------
        print "Entering daily time limit"
        CommonUtil.TakeScreenShot("sModuleInfo")
        result = Set_Text_Field_Value_By_ID(daily_time_id,daily_time_value)
        if result == "failed":
            print "failed to entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "failed to entered the daily time limit", 3)
            CommonUtil.TakeScreenShot("sModuleInfo") 
            return "failed"
        else: 
            print "Successfully entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the daily time limit", 1)

        #----------------
        #Save Configuration 
           
        CommonUtil.ExecLog(sModuleInfo, "Clicking Save Config button",1)
        print "Clicking Save Config button" 
        Click_Element_By_ID(completion_time_id)
        result = Click_Element_By_ID(submit_id) 
        if result == "failed":
            print "failed to click on Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "failed to click on Save Config button", 3)
            return "failed"
        else: 
            print "Successfully clicked Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1)
        CommonUtil.TakeScreenShot("sModuleInfo") 
        #time.sleep(3)
        return "passed"      
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value course settings information.  Error: %s"%Error_Detail, 3)
        print "Unable to set value course settings information"
        return "failed"  


        
def Create_A_New_Course(course_name, short_name, course_id, cleanup='true'):
    '''
    it assumes that you are logged in as Admin
    This function accepts: 
    course_name =  name of the course. 
    cleanup = true if you want to delete old name or false if you want to just keep the name if it already there
    '''
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
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to create course.  Error: %s"%Error_Detail, 3)
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
        CommonUtil.TakeScreenShot("sModuleInfo")
        if on_off == "on":
            print "Checking if Editing is Turned On or Off"
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing is Turned On or Off", 1)
            result = Expand_Menu_By_Name('Front page settings')
            if result == "failed":
                print "Unable to find the menu Front Page settings."
                return "failed"
            expected_text = 'Turn editing'
            try:
                Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text))
            except Exception, e:
                print "Exception : ", e
                print "No option was found to turn Editing on or off"
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3)
                return "failed"
            if (WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text)) ==  'Turn editing off':
                print "Editing is already on"
                CommonUtil.ExecLog(sModuleInfo, "Editing is already on", 1)
                return "passed"
            else:
                print "Turning Editing on"
                result = Click_Element_By_Name('Turn editing on')
                if result == "failed":
                    return "failed"
                else:
                    return "passed"
        elif on_off == "off":
            print "Checking if Editing is Turned On or Off"
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing is Turned On or Off", 1)
            Expand_Menu_By_Name('Front page settings')
            expected_text = 'Turn editing'
            try:
                Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text))
            except Exception, e:
                print "Exception : ", e
                print "No option was found to turn Editing on or off"
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3)
                return "failed"
            if ((WebDriverWait(Element, WebDriver_Wait).until(lambda driver :Element.text))) ==  'Turn editing on':
                print "Editing is already off"
                CommonUtil.ExecLog(sModuleInfo, "Editing is already off", 1)
                return "passed"
            else:
                print "Turning Editing on"
                result = Click_Element_By_Name('Turn editing off')              
                if result == "failed":
                    return "failed"
                else:
                    return "passed"        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "We are unable to control the editing option.  Error: %s"%Error_Detail, 3)
        print "We are unable to control the editing option"
        return "failed"
        
    
def Click_By_Parameter_And_Value(parameter,value, parent=False):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Locating your element...", 1)
        
        if isinstance(parent, (bool)) == True:
            Element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath("//input[@%s='%s']"%(parameter,value)))
        else:
            Element = WebDriverWait(parent, WebDriver_Wait).until(lambda driver :parent.find_element_by_xpath("//input[@%s='%s']"%(parameter,value)))

        CommonUtil.ExecLog(sModuleInfo, "Found element and clicking..", 1)
        Element.click()
        #WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.click())
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked by %s and %"%(parameter,value), 1)
        return "passed" 
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close.  Error: %s"%Error_Detail, 3)
        print "No open browser to close"
        return "failed"
    
def ClickSafety_Course_Settings():
    
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        result = Expand_Menu_By_Name('Site administration')
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3)
            return "failed"        
        #Since below are all under Site Admin, we should restrict our search within Site admin.
        admin_tab = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath("//*[text()='Site administration']"))
        sibling = WebDriverWait(admin_tab, WebDriver_Wait).until(lambda driver :admin_tab.find_element_by_xpath(".."))
        parent = WebDriverWait(sibling, WebDriver_Wait).until(lambda driver :sibling.find_element_by_xpath(".."))
        result = Expand_Menu_By_Name('Plugins',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3)
            return "failed" 
        result = Expand_Menu_By_Name('Local plugins',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3)
            return "failed" 
        result = Expand_Menu_By_Name('ClickSafety',parent)
        if result == 'failed':
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3)
            return "failed"        
        result = Click_Element_By_Name('Course settings',parent) 
        if result == "passed":
            CommonUtil.ExecLog(sModuleInfo, "Click course settings for ClickSafety menu", 1)
            return "passed"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu", 3)
            return "failed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to click course settings for ClickSafety menu.  Error: %s"%Error_Detail, 3)
        print "Unable to click course settings for ClickSafety menu"
        return "failed"    

def Edit_Course_From_Course_Settings(course_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:

        #First we need to find the main table.  From there we will look for course name
        CommonUtil.ExecLog(sModuleInfo, "Locating Course Settings table..", 1)
        table_ = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_id("region-main"))
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Locating your course name...", 1)
        allElements = WebDriverWait(table_, WebDriver_Wait).until(lambda driver :table_.find_elements_by_xpath("//*[text()='%s']"%course_name))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%course_name, 3)
            print "Could not find your course by name: %s"%course_name
            return "failed"
        else:
            if len(allElements) > 1:
                CommonUtil.ExecLog(sModuleInfo, "Found more than one element and will use the first one.  ** if fails, try to locate the element manually ** ", 2)
                print "Found more than one element and will use the first one.  ** if fails, try to locate the element manually ** "
            for each in allElements:
                if (WebDriverWait(each, WebDriver_Wait).until(lambda driver : each.is_displayed())) == True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your course by name: %s.  Using the first element found to click"%course_name, 1)                  
                    print "Found your course by name: %s.  Using the first element to click"%course_name
                    break
        #We need to go one up so we can locate the row ID.  From there we will be able to find the children element for EDIT
        parent = WebDriverWait(Element, WebDriver_Wait).until(lambda driver : Element.find_element_by_xpath(".."))
        Edit_Button = WebDriverWait(parent, WebDriver_Wait).until(lambda driver : parent.find_element_by_xpath("//*[@title='Edit']"))
        Edit_Button.click()
        print "Successfully clicked Edit button for the course: %s"%course_name
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Edit button for the course: %s"%course_name, 1)
        return "passed"                              
        
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "Unable to Edit your course: %s.  Error: %s"%(course_name,Error_Detail), 3)
        print "Unable to Edit your course: %s"%course_name
        return "failed"    

def Tear_Down():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        sBrowser.close()
        print "Successfully closed your browser"
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1)
        return "passed"
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()        
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
        print Error_Detail
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close.  Error: %s"%Error_Detail, 3)
        print "No open browser to close"
        return "failed"

def Delete_A_Course(course_name):
    BrowserSelection('firefox')
    OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    Login('admin','R@1ndrops', 'Admin User')
    Turn_Editing_On_OR_Off('on')
    Expand_Menu_By_Name('Site administration')

    site_admin_element = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_elements_by_xpath("//*[text()='Site administration']"))
    time.sleep(3)
    parent_site_admin = WebDriverWait(site_admin_element, WebDriver_Wait).until(lambda driver : site_admin_element.find_element_by_xpath(".."))
    grand_parent_site_admin = WebDriverWait(parent_site_admin, WebDriver_Wait).until(lambda driver : parent_site_admin.find_element_by_xpath(".."))

    Expand_Menu_By_Name("Courses",grand_parent_site_admin)
    time.sleep(3)
    Click_Element_By_Name('Manage courses and categories',grand_parent_site_admin)

    Set_Text_Field_Value_By_ID('coursesearchbox',course_name)

    Click_By_Parameter_And_Value("value","Go")

    search_course_list = WebDriverWait(sBrowser, WebDriver_Wait).until(lambda driver :sBrowser.find_element_by_xpath("//input[@class='course-listing']"))
    course_element = WebDriverWait(search_course_list, WebDriver_Wait).until(lambda driver :search_course_list.find_elements_by_xpath("//*[text()='%s']"%course_name))
    course_element_row = WebDriverWait(course_element, WebDriver_Wait).until(lambda driver : course_element.find_element_by_xpath(".."))

    Click_By_Parameter_And_Value("alt","Delete",course_element_row)

    
    
    print "Debug"
    
#Delete_A_Course("auto1")

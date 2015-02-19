
import sys
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

def BrowserSelection(browser):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.close()
    except:
        True
    global sBrowser
    try:
        if "Chrome" in browser:
            sBrowser = webdriver.Chrome()
            sBrowser.maximize_window()
            print "Started Chrome Browser"
            CommonUtil.ExecLog(sModuleInfo, "Started Chrome Browser", 1)
            return "PASSED"
        elif browser == 'Firefox':
            sBrowser = webdriver.Firefox()
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Firefox Browser", 1)
            print "Started Firefox Browser"
            return "PASSED"
        elif "IE" in browser:
            sBrowser = webdriver.Ie()
            sBrowser.maximize_window()
            CommonUtil.ExecLog(sModuleInfo, "Started Internet Explorer Browser", 1)
            print "Started Internet Explorer Browser"
            return "PASSED"
        else:
            print "You did not select a valid browser: %s" % browser
            CommonUtil.ExecLog(sModuleInfo, "You did not select a valid browser: %s" % browser, 3)
            return "Failed"
        time.sleep(3)
    except Exception, e:
        print "Exception : ", e
        print "Unable to start WebDriver"
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver", 3)
        return "Failed"

def OpenLink(link, page_title):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.get(link)
        WebDriverWait(sBrowser, 30)
        CommonUtil.ExecLog(sModuleInfo, "Successfully opened your link: %s" % link, 1)
        print "Successfully opened your link: " + link
        CommonUtil.TakeScreenShot("sModuleInfo")
        assert page_title in sBrowser.title
        time.sleep(3)
        return "PASSED"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Failed to open your link: %s" % link, 3)
        print "Failed to open your link: %s" % link
        CommonUtil.TakeScreenShot("sModuleInfo")
        return "Failed"

def Login(user_name,password):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        
        
        CommonUtil.TakeScreenShot("sModuleInfo")
        elem = sBrowser.find_element_by_link_text("Log in")
        elem.send_keys(Keys.RETURN)
        sBrowser.implicitly_wait(20)
        elem = sBrowser.find_element_by_id("username")
        elem.send_keys(user_name)
        elem = sBrowser.find_element_by_id("password")
        elem.send_keys(password)
        elem = sBrowser.find_element_by_id("loginbtn")
        elem.send_keys(Keys.RETURN)
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully logged in", 1)
        print "Successfully logged in"
        time.sleep(3)
        return "PASSED"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to login", 3)
        print "Unable to login"
        return "Failed"
    
def Expand_Menu_By_Name_OR_ID(name_or_id_or_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%name_or_id_or_id, 1)
        print "Trying to find element by name: %s"%name_or_id_or_id
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (name_or_id_or_id))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%name_or_id_or_id, 2)
            print "Could not find your element by name: %s"%name_or_id_or_id
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%name_or_id_or_id, 1)
            print "Trying to find element by ID: %s"%name_or_id_or_id
            try:
                Element = sBrowser.find_element_by_id(name_or_id_or_id)   
                CommonUtil.ExecLog(sModuleInfo, "Found your element by ID: %s"%name_or_id_or_id, 1)
                print "Found your element by ID: %s"%name_or_id_or_id
            except:
                CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%name_or_id_or_id, 3)
                print "Could not find your element by name or ID: %s"%name_or_id_or_id
                return "Failed"
        #Now find the ones that are being displayed
        else:
            for each in allElements:
                if each.is_displayed() ==True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%name_or_id_or_id, 1)
                    print "Found your element by name: %s.  Using the first element found to click"%name_or_id_or_id                   
                    break
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        parent = Element.find_element_by_xpath("..")
        grand_parent = parent.find_element_by_xpath("..")
        expand_status = grand_parent.get_attribute("aria-expanded")
        expand_status = str(expand_status).lower()
        if expand_status == 'true':
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%name_or_id_or_id, 2)
            print "%s is already expanded "%name_or_id_or_id
            return "PASSED"
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%name_or_id_or_id, 1)
            sBrowser.implicitly_wait(20)
            Element.click()
            time.sleep(5)
        #Verify if it was expanded 
        expand_status = grand_parent.get_attribute("aria-expanded")
        expand_status = str(expand_status).lower()
        if (expand_status== "true"):
            CommonUtil.TakeScreenShot("sModuleInfo")
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%name_or_id_or_id, 1)
            time.sleep(3)
            print "Successfully expanded your menu: %s"%name_or_id_or_id
            return "PASSED"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%name_or_id_or_id, 3)
            print "Unable to expand Menu: %s"%name_or_id_or_id
            return "Failed"   
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%name_or_id_or_id, 3)
        print "Unable to expand Menu: %s"%name_or_id_or_id
        return "Failed"    




def Click_Element_By_Name_OR_ID(name_or_id):
    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%name_or_id, 1)
        print "Trying to find element by name: %s"%name_or_id
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (name_or_id))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%name_or_id, 2)
            print "Could not find your element by name: %s"%name_or_id
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%name_or_id, 1)
            print "Trying to find element by ID: %s"%name_or_id
            try:
                Element = sBrowser.find_element_by_id(name_or_id)   
            except:
                CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%name_or_id, 3)
                print "Could not find your element by name or ID: %s"%name_or_id
                return "Failed"
        else:
            for each in allElements:
                if each.is_displayed() ==True:
                    Element = each
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%name_or_id, 1)
                    print "Found your element by name: %s.  Using the first element found to click"%name_or_id                   
                    break   
        #Now we simply click it
        sBrowser.implicitly_wait(20)
        Element.click()
        time.sleep(5)
        print "Successfully clicked your element by name or ID: %s"%name_or_id
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%name_or_id, 1)
        return "PASSED"

    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%name_or_id, 3)
        print "Unable to expand Menu: %s"%name_or_id
        return "Failed"    

def Set_Text_Field_Value_By_ID(id,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by id: %s"%id, 1)
        print "Trying to find element by id: %s"%id
        try:
            Element = sBrowser.find_element_by_id(id)   
        except:
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by ID: %s"%id, 3)
            print "Could not find your element by ID: %s"%id
            return "Failed"  
        #Now we simply click it
        sBrowser.find_element_by_id(id).click()
        sBrowser.find_element_by_id(id).clear()
        sBrowser.find_element_by_id(id).send_keys(value)
        sBrowser.implicitly_wait(20)
        Element.click()
        time.sleep(5)
        print "Successfully set the value of to text with ID: %s"%id
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully set the value of to text with ID: %s"%id, 1)
        return "PASSED"

    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value for your ID: %s"%id, 3)
        print "Unable to set value for your ID: %s"%id
        return "Failed"    

def Click_Element_By_Custome_Field_Value(field,value):
    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by field: %s and value: %s"%(field,value), 1)
        print "Trying to find element by field: %s and value: %s"%(field,value)
        Element = sBrowser.find_element_by_xpath("//input[@%s='%s']"%(field,value))
        #Now we simply click it
        sBrowser.implicitly_wait(20)
        Element.click()
        time.sleep(5)
        print "Successfully clicked your element by field: %s and value: %s"%(field,value)
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element by field: %s and value: %s"%(field,value), 1)
        return "PASSED"

    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to click your element by field: %s and value: %s"%(field,value), 3)
        print "Unable to click your element by field: %s and value: %s"%(field,value)
        return "Failed"    



def Verify_Text_Message_By_Class(element, expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1)
        print "Getting text string from the web"
        Elem = sBrowser.find_element_by_class_name("message")
        actual_text = Elem.text
        if actual_text == expected_text:
            print "Successfully verified your text: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1)
            print "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1)
            time.sleep(3)
            return "PASSED"            
        else:
            print "Failed to verify your expected text: %s"%expected_text
            CommonUtil.ExecLog(sModuleInfo, "Failed to verify your expected text: %s"%expected_text, 3)
            print "Expected text was:'%s' but Actual text was '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text was:'%s' but Actual text was '%s' "%(expected_text,actual_text), 3)
            return "Failed"

     
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Error occur during verification process", 3)
        print "Error occur during verification process"
        return "Failed"  


def Course_Exists(course):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Searching for course: %s"%course, 1)
        print "Searching for course: %s"%course
        Elem = sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %course)
        actual_text = Elem.text
       
        if actual_text == course:
            print "Successfully verified that course exists: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified that course exists: %s"%actual_text, 1)
            time.sleep(3)
            return "PASSED"            
     
    except Exception, e:
        #print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Could not find your course: %s"%course, 3)
        print "Could not find your expected course: %s"%course
        return "Failed"  
    


def Verify_Text_Message_By_Text(expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Getting text string from the web", 1)
        print "Getting text string from the web"
        Elem = sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text)
        actual_text = Elem.text
        if actual_text == expected_text:
            print "Successfully verified your text: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 1)
            print "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 1)
            time.sleep(3)
            return "PASSED"            
     
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Could not find your expected text: %s"%expected_text, 3)
        print "Could not find your expected text: %s"%expected_text
        return "Failed"  


def Course_Settings_Time_Limit(completion_time_id, completion_time_value,daily_time_id, daily_time_value,submit_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Entering completion time in minutes", 1)
        print "Entering completion time in minutes"
        result = Set_Text_Field_Value_By_ID(completion_time_id,completion_time_value)
        if result == "Failed":
            print "Failed to entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "Failed to entered the completion time value", 3)
            CommonUtil.TakeScreenShot("sModuleInfo")
            return "Failed"
        else: 
            print "Successfully entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the completion time value", 1)

        #----------------
        print "Entering daily time limit"
        CommonUtil.TakeScreenShot("sModuleInfo")
        result = Set_Text_Field_Value_By_ID(daily_time_id,daily_time_value)
        if result == "Failed":
            print "Failed to entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "Failed to entered the daily time limit", 3)
            CommonUtil.TakeScreenShot("sModuleInfo") 
            return "Failed"
        else: 
            print "Successfully entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the daily time limit", 1)

        #----------------
        #Save Configuration 
           
        CommonUtil.ExecLog(sModuleInfo, "Clicking Save Config button",1)
        print "Clicking Save Config button" 
           
        result = Click_Element_By_Name_OR_ID(submit_id) 
        if result == "Failed":
            print "Failed to click on Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "Failed to click on Save Config button", 3)
            return "Failed"
        else: 
            print "Successfully clicked Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1)
        CommonUtil.TakeScreenShot("sModuleInfo") 
        time.sleep(3)
        return "PASSED"      
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value course settings information", 3)
        print "Unable to set value course settings information"
        return "Failed"  


def Delete_A_Course(course_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name   
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")

        print "Successfully closed your browser"
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1)
        return "PASSED"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close", 3)
        print "No open browser to close"
        return "Failed"
        
def Create_A_New_Course(course_name, short_name, course_id, cleanup='true'):
    '''
    it assumes that you are logged in as Admin
    This function accepts: 
    course_name =  name of the course. 
    cleanup = true if you want to delete old name or false if you want to just keep the name if it already there
    '''

    Click_Element_By_Name_OR_ID('Home')
    
    course_exists = Course_Exists(course_name)
    if (course_exists == "PASSED") and (cleanup=='true'):
        print "Existing course found and will be deleted"
        result = Delete_A_Course(course_name)
        if result == "Failed":
            print "Unable to delete an existing course"
            return "Failed"
    elif (course_exists == "PASSED") and (cleanup!='true'):
        print "Course already exists and clean up was set not to re-create"
        return "PASSED"
    else:
        print "Course name was not found and will be created"
            
    
    Turn_Editing_On_OR_Off("on")
    Expand_Menu_By_Name_OR_ID('Site administration')
    Expand_Menu_By_Name_OR_ID('yui_3_15_0_3_1424235876713_5248')
    Click_Element_By_Name_OR_ID('Manage courses and categories')
    Click_Element_By_Name_OR_ID('Miscellaneous')
    Click_Element_By_Name_OR_ID('Create new course')
    Set_Text_Field_Value_By_ID('id_fullname',course_name)
    Set_Text_Field_Value_By_ID('id_shortname',short_name)
    Set_Text_Field_Value_By_ID('id_idnumber',course_id)
    
    Click_By_Parameter_And_Value("value","Save changes")
    course_name_verify = "%s: 0 enrolled users"%course_name
    Verify_Text_Message_By_Text(course_name_verify)

    Tear_Down()  

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
            result = Expand_Menu_By_Name_OR_ID('Front page settings')
            if result == "Failed":
                print "Unable to find the menu Front Page settings."
                return "Failed"
            expected_text = 'Turn editing'
            try:
                Elem = sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text)
            except Exception, e:
                print "Exception : ", e
                print "No option was found to turn Editing on or off"
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3)
                return "Failed"
            if (Elem.text) ==  'Turn editing off':
                print "Editing is already on"
                CommonUtil.ExecLog(sModuleInfo, "Editing is already on", 1)
                return "PASSED"
            else:
                print "Turning Editing on"
                result = Click_Element_By_Name_OR_ID('Turn editing on')
                if result == "Failed":
                    return "Failed"
                else:
                    return "Passed"
        elif on_off == "off":
            print "Checking if Editing is Turned On or Off"
            CommonUtil.ExecLog(sModuleInfo, "Checking if Editing is Turned On or Off", 1)
            Expand_Menu_By_Name_OR_ID('Front page settings')
            expected_text = 'Turn editing'
            try:
                Elem = sBrowser.find_element_by_xpath ("//*[contains(text(),'%s')]" %expected_text)
            except Exception, e:
                print "Exception : ", e
                print "No option was found to turn Editing on or off"
                CommonUtil.ExecLog(sModuleInfo, "No option was found to turn Editing on or off", 3)
                return "Failed"
            if (Elem.text) ==  'Turn editing on':
                print "Editing is already off"
                CommonUtil.ExecLog(sModuleInfo, "Editing is already off", 1)
                return "PASSED"
            else:
                print "Turning Editing on"
                result = Click_Element_By_Name_OR_ID('Turn editing off')              
                if result == "Failed":
                    return "Failed"
                else:
                    return "Passed"        
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "We are unable to control the editing option", 3)
        print "We are unable to control the editing option"
        return "Failed"
        
    
def Click_By_Parameter_And_Value(parameter,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Locating your element...", 1)
        Elem = sBrowser.find_element_by_xpath("//input[@%s='%s']"%(parameter,value))
        CommonUtil.ExecLog(sModuleInfo, "Found element and clicking..", 1)
        Elem.click()
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked by %s and %"%(parameter,value), 1)
        time.sleep(3)
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close", 3)
        print "No open browser to close"
        return "Failed"
    


def Tear_Down():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        sBrowser.close()
        print "Successfully closed your browser"
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 1)
        return "PASSED"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close", 3)
        print "No open browser to close"
        return "Failed"


# BrowserSelection('Firefox')
# OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
# Login('admin','R@1ndrops')
# Expand_Menu_By_Name_OR_ID('Site administration')
# Create_A_New_Course("AutomationCourse", "AS", "ASID")



from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.selenium as Sal
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from CoreFrameWork import CommonUtil
#Ver1.0
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sys
sys.path.append("..")

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
        CommonUtil.ExecLog(sModuleInfo, "Successfully logged in", 3)
        print "Successfully logged in"
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
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%name_or_id_or_id, 3)
        print "Trying to find element by name: %s"%name_or_id_or_id
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (name_or_id_or_id))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%name_or_id_or_id, 3)
            print "Could not find your element by name: %s"%name_or_id_or_id
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%name_or_id_or_id, 3)
            print "Trying to find element by ID: %s"%name_or_id_or_id
            try:
                Element = sBrowser.find_element_by_id(name_or_id_or_id)   
                CommonUtil.ExecLog(sModuleInfo, "Found your element by ID: %s"%name_or_id_or_id, 3)
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
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%name_or_id_or_id, 3)
                    print "Found your element by name: %s.  Using the first element found to click"%name_or_id_or_id                   
                    break
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        parent = Element.find_element_by_xpath("..")
        grand_parent = parent.find_element_by_xpath("..")
        expand_status = grand_parent.get_attribute("aria-expanded")
        if grand_parent.get_attribute("aria-expanded") == True:
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%name_or_id_or_id, 3)
            print "%s is already expanded "%name_or_id_or_id
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%name_or_id_or_id, 3)
            sBrowser.implicitly_wait(20)
            Element.click()
            time.sleep(5)
        #Verify if it was expanded 
        expand_status = grand_parent.get_attribute("aria-expanded")
        if (expand_status== "true") or (expand_status == True):
            CommonUtil.TakeScreenShot("sModuleInfo")
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%name_or_id_or_id, 3)
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
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by name: %s"%name_or_id, 3)
        print "Trying to find element by name: %s"%name_or_id
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (name_or_id))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%name_or_id, 3)
            print "Could not find your element by name: %s"%name_or_id
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%name_or_id, 3)
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
                    CommonUtil.ExecLog(sModuleInfo, "Found your element by name: %s.  Using the first element found to click"%name_or_id, 3)
                    print "Found your element by name: %s.  Using the first element found to click"%name_or_id                   
                    break   
        #Now we simply click it
        sBrowser.implicitly_wait(20)
        Element.click()
        time.sleep(5)
        print "Successfully clicked your element by name or ID: %s"%name_or_id
        return "PASSED"
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%name_or_id, 3)
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%name_or_id, 3)
        print "Unable to expand Menu: %s"%name_or_id
        return "Failed"    

def Set_Text_Field_Value_By_ID(id,value):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Trying to find element by id: %s"%id, 3)
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
        return "PASSED"
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully set the value of to text with ID: %s"%id, 3)
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value for your ID: %s"%id, 3)
        print "Unable to set value for your ID: %s"%id
        return "Failed"    

def Verify_Text_Message_By_Class(element, expected_text):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Entering completion time in minutes", 3)
        print "Getting text string from the web"
        Elem = sBrowser.find_element_by_class_name("message")
        actual_text = Elem.text
        if actual_text == expected_text:
            print "Successfully verified your text: %s"%actual_text
            CommonUtil.ExecLog(sModuleInfo, "Successfully verified your text: %s"%actual_text, 3)
            print "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text)
            CommonUtil.ExecLog(sModuleInfo, "Expected text is:'%s' and Actual text is '%s' "%(expected_text,actual_text), 3)
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


def Course_Settings_Time_Limit(completion_time_id, completion_time_value,daily_time_id, daily_time_value,submit_id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Entering completion time in minutes", 3)
        print "Entering completion time in minutes"
        result = Set_Text_Field_Value_By_ID(completion_time_id,completion_time_value)
        if result == "Failed":
            print "Failed to entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "Failed to entered the completion time value", 3)
            return "Failed"
        else: 
            print "Successfully entered the completion time value"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the completion time value", 3)
        CommonUtil.TakeScreenShot("sModuleInfo")
        #----------------
        print "Entering daily time limit"
        CommonUtil.TakeScreenShot("sModuleInfo")
        result = Set_Text_Field_Value_By_ID(daily_time_id,daily_time_value)
        if result == "Failed":
            print "Failed to entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "Failed to entered the daily time limit", 3)
            return "Failed"
        else: 
            print "Successfully entered the daily time limit"
            CommonUtil.ExecLog(sModuleInfo, "Successfully entered the daily time limit", 3)
        CommonUtil.TakeScreenShot("sModuleInfo") 
        #----------------
        #Save Configuration 
           
        CommonUtil.ExecLog(sModuleInfo, "Clicking Save Config button"  , 3)
        print "Clicking Save Config button"    
        result = Click_Element_By_Name_OR_ID(submit_id) 
        if result == "Failed":
            print "Failed to click on Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "Failed to click on Save Config button", 3)
            return "Failed"
        else: 
            print "Successfully clicked Save Config button"
            CommonUtil.ExecLog(sModuleInfo, "Successfully clicked Save Config button", 3)
        
        return "PASSED"      
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to set value course settings information", 3)
        print "Unable to set value course settings information"
        return "Failed"  


def Tear_Down():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        sBrowser.close()
        print "Successfully closed your browser"
        CommonUtil.TakeScreenShot("sModuleInfo")
        return "PASSED"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "No open browser to close", 3)
        print "No open browser to close"
        return "Failed"

def Repurchase_the_course_when_the_final_exam_is_failed_for_third_time():
    #make your test cases by re-using same steps
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops')
    print Click_Element_By_Name_OR_ID('Turn editing on')
    print Expand_Menu_By_Name_OR_ID('Site administration')
    print Expand_Menu_By_Name_OR_ID('Plugins')
    print Expand_Menu_By_Name_OR_ID('Local plugins')
    print Expand_Menu_By_Name_OR_ID('ClickSafety')
    print Click_Element_By_Name_OR_ID('Course settings')
    print Click_Element_By_Name_OR_ID('Edit')
    print Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    print Verify_Text_Message_By_Class('message', 'Updated successfully')
    print Tear_Down()


def Test_Suite():
    #add additional test cases
    Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()

Test_Suite()



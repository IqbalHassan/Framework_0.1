
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.selenium as Sal
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from AutomationFW import CommonUtil
#Ver1.0
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
    
def Expand_Menu_By_Name_OR_ID(menu_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%menu_name, 3)
            print "Could not find your element by name: %s"%menu_name
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%menu_name, 3)
            print "Trying to find element by ID: %s"%menu_name
            try:
                Element = sBrowser.find_element_by_id(menu_name)   
            except:
                CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%menu_name, 3)
                print "Could not find your element by name or ID: %s"%menu_name
                return "Failed"
        #Now find the ones that are being displayed
        else:
            for each in allElements:
                if each.is_displayed() ==True:
                    Element = each
                    break
        #Now we need to find out if it is expanded.  To do this we need to go two level up 
        parent = Element.find_element_by_xpath("..")
        grand_parent = parent.find_element_by_xpath("..")
        expand_status = grand_parent.get_attribute("aria-expanded")
        if grand_parent.get_attribute("aria-expanded") == True:
            CommonUtil.ExecLog(sModuleInfo, "%s is already expanded "%menu_name, 3)
            print "%s is already expanded "%menu_name
        else:
            CommonUtil.ExecLog(sModuleInfo, "%s is not expanded. Expanding.. "%menu_name, 3)
            sBrowser.implicitly_wait(20)
            Element.click()
            time.sleep(5)
        #Verify if it was expanded 
        expand_status = grand_parent.get_attribute("aria-expanded")
        if (expand_status== "true") or (expand_status == True):
            CommonUtil.TakeScreenShot("sModuleInfo")
            CommonUtil.ExecLog(sModuleInfo, "Successfully to expand menu: %s"%menu_name, 3)
            print "Successfully to expand menu: %s"%menu_name
            return "PASS"
        else:
            CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%menu_name, 3)
            print "Unable to expand Menu: %s"%menu_name
            return "Failed"   
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%menu_name, 3)
        print "Unable to expand Menu: %s"%menu_name
        return "Failed"    


def Click_Element_By_Name_OR_ID(element_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        CommonUtil.TakeScreenShot("sModuleInfo")
        #Find all elements containing the name
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (element_name))
        if allElements == []:        
            CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name: %s"%element_name, 3)
            print "Could not find your element by name: %s"%element_name
            CommonUtil.ExecLog(sModuleInfo, "Trying to find element by ID: %s"%element_name, 3)
            print "Trying to find element by ID: %s"%element_name
            try:
                Element = sBrowser.find_element_by_id(element_name)   
            except:
                CommonUtil.ExecLog(sModuleInfo, "Could not find your element by name or ID: %s"%element_name, 3)
                print "Could not find your element by name or ID: %s"%element_name
                return "Failed"
        else:
            for each in allElements:
                if each.is_displayed() ==True:
                    Element = each
                    break   
        #Now we simply click it
        sBrowser.implicitly_wait(20)
        Element.click()
        time.sleep(5)
        return "PASS"
        CommonUtil.TakeScreenShot("sModuleInfo")
        CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your element: %s"%element_name, 3)
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to expand menu: %s"%element_name, 3)
        print "Unable to expand Menu: %s"%element_name
        return "Failed"    

def CloseBrowser():
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

def TestCase1():
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
    print CloseBrowser()


def Test_Suite():
    #add additional test cases
    TestCase1()

#Uncomment this to run test cases
#Test_Suite()    
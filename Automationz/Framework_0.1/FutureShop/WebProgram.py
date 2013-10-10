'''
Created on Sep 22, 2013

@author: Riz
'''
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.selenium as Sal
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def FindElement(sBrowser, sFindBy, sValue):
    try:
        if sFindBy == "xpath":
            element = WebDriverWait(sBrowser, 8).until(lambda driver : sBrowser.find_element_by_xpath(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element
        if sFindBy == "class_name":
            element = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_class_name(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element
        if sFindBy == "css_selector":
            element = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_css_selector(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element
        if sFindBy == "id":
            element = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_id(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element
        if sFindBy == "link_text":
            element = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_link_text(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element
        if sFindBy == "name":
            element = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_name(sValue))
            WebDriverWait(sBrowser, 8).until(lambda driver : element.is_displayed())
            return element

    except Exception, e:
        print e
        return False





#from webdriverplus import WebDriver
#browser = WebDriver('firefox',quit_on_exit=False)
#
#browser.get('http://www.futureshop.ca')
#
#print browser



#sBrowser = webdriver.Firefox()
#sBrowser.get('http://www.futureshop.ca/en-CA/category/laptops-macbooks/1002.aspx?path=847316bb9e1ba03338d63d9ec2954796en01')
#sBrowser.get('http://www.futureshop.ca')


#print sBrowser.find_elements_by_link_text("iPad & Tablets")



def BrowserSelection(browser):
    global sBrowser
    print "browser:%s:" % browser
    try:
        if browser == 'Chrome':
            sBrowser = webdriver.Chrome()
            print "Started Chrome Browser"
            return "Pass"
        elif browser == 'Firefox':
            sBrowser = webdriver.Firefox()
            print "Started Chrome Browser"
            return "Pass"
        elif browser == 'IE':
            sBrowser = webdriver.Ie()
            print "Started Chrome Browser"
            return "Pass"
        else:
            print "not a valid browser selection"
            return "Critical"
    except:
        print "Unable to start WebDriver"
        return "Critical"

def OpenLink(link):
    try:
        print sBrowser
    except:
        print "this sBrowser doesnt exists"
    
    try:
        #print sBrowser
        sBrowser.get(link)
        print "successfully opened browser: " + link
        return "Pass"
    except:
        print "unable to open browser: " + link
        return "Critical"

def SelectFirstLevelMenu(menu_name_1):
    try:
        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements) == 0:
            print "Unable to find your main menu object"
            return "Critical"
        for element in allElements:
            if menu_name_1 == element.text:
                print "Found the Main Menu: " + element.text
                result = HoeverOver(element)
                if result != "Pass":
                    return "Critical"
                else:
                    return "Pass"
        print "Unable to find your element: " + menu_name_1
        return "Critical"
    except:
        print "Error trying to select the main menu"
        return "Critical"


def SelectSecondLevelMenu(menu_name_2):
    try:
        #menu_name_2 = "filter-"+ (check_box_name.replace(" ", "-")).lower()

        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements) == 0:
            print "Unable to find your main menu object"
            return "Critical"
        for element in allElements:
            if menu_name_2 == element.text:
                print "Found the Main Menu: " + element.text
                result = HoeverOver(element)
                if result != "Pass":
                    return "Critical"
                else:
                    return "Pass"
        print "Unable to find your element: " + menu_name_2
        return "Critical"
    except:
        print "Error trying to select the second level menu"
        return "Critical"

def SelectThirdLevelMenu(menu_name_3):
    try:
        allElements = sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name_3))
        for eachElements in allElements:
            if  menu_name_3 == eachElements.get_attribute("text"):
                print "Found your selection: " + menu_name_3
                sBrowser.get(eachElements.get_attribute('href'))
                print "Successfully clicked your item: " + menu_name_3
                return "Pass"
        print "Unable to find your item to click: " + menu_name_3
        return "Critical"
    except:
        print "Error trying to select the main menu"
        return "Critical"



def HoeverOver(element):
    try:
        print "Hovering over to the element " + (element.text)
        hov = ActionChains(sBrowser).move_to_element(element)
        hov.perform()
        return "Pass"
    except:
        print "Unable to hover over the element"
        return "Critical"

def FilterBySelection(check_box_name):
    try:

        check_box = "filter-" + (check_box_name.replace(" ", "-")).lower()

        for elem in sBrowser.find_elements_by_xpath('.//li[@class="%s"]' % check_box):
            print 'Your check box %s is found but it is currently not checked' % check_box_name
            for elem in sBrowser.find_elements_by_xpath('.//span[@class = "item"]'):
                if elem.text == check_box_name:
                    elem.click()
                    time.sleep(5)
                    print "Your check box: %s is now checked" % check_box_name
                    return "Pass"
        #Verify if check box was already checked
        if_check_box_checked = check_box + " is-selected"
        #for elem in sBrowser.find_elements_by_xpath('.//li[@class = "filter-on-sale is-selected"]'):
        for elem in sBrowser.find_elements_by_xpath('.//li[@class="%s"]' % if_check_box_checked):
            print "your check box was already selected"
            return "Pass"
        print "Unable to locate your check box: %s" % check_box_name
        return "Critical"

    except:
        print "Unable to select your check box: %s" % check_box_name


def RemoveFilter(check_box_name):
    print 'checkbox'




def GetFilterCount(check_box_name):
    try:
        #Since checkbox name changes dynamically when you select, we need to first 
        #try to see if it works with unchecked name and then we will try with 
        #checked name
        unchecked_name = "filter-" + (check_box_name.replace(" ", "-")).lower()
        checked_name = unchecked_name + " is-selected"
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]' % unchecked_name)
        #check_box_name = check_box_name_count.find_element_by_xpath('.//span[@class="item"]')
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        #check_box_status = check_box_name_count.find_element_by_xpath('.//input[@type="checkbox"]')
        print "Found your checkbox and the count is: %s" % check_box_count.text
        replace1 = (check_box_count.text).replace("(", "")
        return replace1.replace(")", "")
    except:
        print "Unable to find the check box.  It may be checked.  I will try to find if check box is checked"
    try:
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]' % checked_name)
        #check_box_name = check_box_name_count.find_element_by_xpath('.//span[@class="item"]')
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        #check_box_status = check_box_name_count.find_element_by_xpath('.//input[@type="checkbox"]')
        print "Found your checkbox.  It was checked.  Your count is: %s" % check_box_count.text
        replace1 = (check_box_count.text).replace("(", "")
        return replace1.replace(")", "")
    except:
        print "Unable to find the check box"
        return "Critical"












#print BrowserSelection('Firefox')
#print OpenLink('http://www.futureshop.ca')
#print SelectFirstLevelMenu ('Departments')
#print SelectSecondLevelMenu('Computers & Software')
#print SelectThirdLevelMenu('iPad & Tablets')
##print SelectThirdLevelMenu('Software')
#print FilterBySelection("On Sale")
#print GetFilterCount("On Sale")

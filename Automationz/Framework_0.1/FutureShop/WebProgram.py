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
import CommonUtil

def BrowserSelection(browser): 
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    global sBrowser
    try:
        if browser == 'Chrome':
            sBrowser = webdriver.Chrome()
            print "Started Chrome Browser"
            CommonUtil.ExecLog(sModuleInfo, "Started Chrome Browser", 1)
            return "PASS"
        elif browser == 'Firefox':
            sBrowser = webdriver.Firefox()
            CommonUtil.ExecLog(sModuleInfo, "Started Firefox Browser", 1)
            print "Started Firefox Browser"
            return "PASS"
        elif browser == 'IE':
            sBrowser = webdriver.Ie()
            CommonUtil.ExecLog(sModuleInfo, "Started Internet Explorer Browser", 1)
            print "Started Internet Explorer Browser"
            return "PASS"
        else:
            print "You did not select a valid browser"
            CommonUtil.ExecLog(sModuleInfo, "You did not select a valid browser", 3)
            return "Critical"
    except Exception, e:
        print "Exception : ", e
        print "Unable to start WebDriver"
        CommonUtil.ExecLog(sModuleInfo, "Unable to start WebDriver", 3)
        return "Critical"

def OpenLink(link):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        sBrowser.get(link)
        WebDriverWait(sBrowser, 30)
        CommonUtil.ExecLog(sModuleInfo, "Successfully opened your link: %s"%link, 1)
        print "Successfully opened your link: " +link
        return "PASS"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Failed to open your link: %s"%link, 3)
        print "Failed to open your link: %s"%link
        return "Critical"

def SelectFirstLevelMenu(menu_name_1):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements)== 0:
            print "Unable to find your main menu object"
            CommonUtil.ExecLog(sModuleInfo, "Unable to find your main menu object: %s"%menu_name_1, 3)
            return "Critical"
        for element in allElements:
            if menu_name_1 == element.text:
                CommonUtil.ExecLog(sModuleInfo, "Found your main menu item: %s"%element.text, 1)
                print "Found the Main Menu: " + element.text
                result = HoeverOver(element)
                CommonUtil.ExecLog(sModuleInfo, "Hovering over to your main menu: %s"%menu_name_1, 1)
                if result != "PASS":
                    CommonUtil.ExecLog(sModuleInfo, "Unable to hover over your main menu: %s"%menu_name_1, 3)
                    return "Critical"
                else: 
                    CommonUtil.ExecLog(sModuleInfo, "Successfully hovered over your main menu: %s"%menu_name_1, 1)
                    return "PASS" 
        print "Unable to find your element: " + menu_name_1
        CommonUtil.ExecLog(sModuleInfo, "Unable to find your main menu object: %s"%menu_name_1, 3)
        return "Critical"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Error trying to select the main menu: %s"%menu_name_1, 3)
        print "Error trying to select the main menu"
        return "Critical"
        
                
def SelectSecondLevelMenu(menu_name_2):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements)== 0:
            print "Unable to find your second level menu object"
            CommonUtil.ExecLog(sModuleInfo, "Unable to find your second level menu object: %s"%menu_name_2, 3)
            return "Critical"
        for element in allElements:
            if menu_name_2 == element.text:
                print "Found the second level menu: " + element.text
                CommonUtil.ExecLog(sModuleInfo, "Found the second level menu:  %s"%menu_name_2, 3)
                CommonUtil.ExecLog(sModuleInfo, "Hovering over to your second level menu: %s"%menu_name_2, 1)
                result = HoeverOver(element)
                if result != "PASS":
                    CommonUtil.ExecLog(sModuleInfo, "Unable to hover over your second level element: %s"%menu_name_2, 3)
                    return "Critical"
                else: 
                    CommonUtil.ExecLog(sModuleInfo, "Successfully hovered over your second level menu: %s"%menu_name_2, 1)
                    return "PASS" 
        print "Unable to find your element: " + menu_name_2
        CommonUtil.ExecLog(sModuleInfo, "Unable to find second level menu item: %s"%menu_name_2, 3)
        return "Critical"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Error trying to select the second level menu: %s"%menu_name_2, 3)
        print "Error trying to select the second level menu"
        return "Critical"

def SelectThirdLevelMenu(menu_name_3):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        allElements= sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name_3))
        for eachElements in allElements:            
            if  menu_name_3 == eachElements.get_attribute("text"):
                print "Found your selection: " +  menu_name_3              
                sBrowser.get(eachElements.get_attribute('href'))
                print "Successfully clicked your item: " + menu_name_3
                CommonUtil.ExecLog(sModuleInfo, "Successfully clicked your item: %s"%menu_name_3, 1)
                return "PASS"
        print "Unable to find your item to click: " + menu_name_3
        CommonUtil.ExecLog(sModuleInfo, "Unable to find your item to click: %s"%menu_name_3, 3)
        return "Critical"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Error trying to select the 3rd level menu: %s"%menu_name_3, 3)
        print "Error trying to select the 3rd level menu"
        return "Critical"
        

def HoeverOver(element):     
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name  
    '''
    All log reporting should be done from the modules that is calling this guy.  This way we do not duplicate our logging
    Since this is a action and not a step, the logging must be done from the steps point of view
    '''
    try:
        print "Hovering over to the element " + (element.text)
        hov = ActionChains(sBrowser).move_to_element(element)
        hov.perform()
        return "PASS"
    except:
        print "Unable to hover over the element"
        return "Critical"
        
def FilterBySelection(check_box_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        
        check_box = "filter-"+ (check_box_name.replace(" ", "-")).lower()
        '''  
        .// will allow us to look at only limited depth
        WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_name(sValue))
        all_elements = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%check_box))
        
        This funciton should be updated with:
        find_elements_by_xpath ("//*[contains(text(),'%s')]"
        '''
        for elem in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%check_box))):
            print 'Your check box %s is found but it is currently not checked' %check_box_name
            CommonUtil.ExecLog(sModuleInfo, "Your check box %s is found but it is currently not checked" %check_box_name, 3)
            for elem in sBrowser.find_elements_by_xpath('.//span[@class = "item"]'):
                if elem.text == check_box_name:
                    elem.click()
                    time.sleep(5)
                    print "Your check box: %s is now checked" %check_box_name
                    CommonUtil.ExecLog(sModuleInfo, "Your check box: %s is now checked" %check_box_name, 3)
                    return "PASS"
        '''
        Verify if check box was already checked
        '''
        if_check_box_checked = check_box + " is-selected"
        for elem in sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%if_check_box_checked):
            print "your check box was already selected"
            CommonUtil.ExecLog(sModuleInfo, "Your check box %s was already selected." %check_box_name, 3)
            return "PASS"
        print "Unable to locate your check box: %s"  %check_box_name 
        CommonUtil.ExecLog(sModuleInfo, "Unable to locate your check box: %s" %check_box_name, 3)
        return "Critical"
        
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Unable to select your check box: %s" %check_box_name, 3)
        print "Unable to select your check box: %s" %check_box_name
        return "Critical"


def RemoveFilter(check_box_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    print 'checkbox'  
    return "PASS"          




def GetFilterCount(check_box_name):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        '''
        This function is an action that other steps and module will call.  Please do not add logging to this module
        you should instead rely on the return value to do your logging
        
        Since checkbox name changes dynamically when you select, we need to first 
        try to see if it works with unchecked name and then we will try with checked name
        this code needs to be updated with: find_elements_by_xpath ("//*[contains(text(),'%s')]"
        This will effectively find the detail of the check box name and stats of the checkbox
        '''
        unchecked_name = "filter-"+ (check_box_name.replace(" ", "-")).lower()
        checked_name  = unchecked_name + " is-selected"
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]'%unchecked_name)
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        print "Found your checkbox and the count is: %s" %check_box_count.text
        replace1 =(check_box_count.text).replace("(", "")
        return replace1.replace(")","")
    except:
        print "Unable to find the check box.  It may be checked.  I will try to find if check box is checked"
    try:
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]'%checked_name)
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        print "Found your checkbox.  It was checked.  Your count is: %s" %check_box_count.text
        replace1 =(check_box_count.text).replace("(", "")
        return replace1.replace(")","")
    except:
        print "Unable to find the check box"
        return "Critical"

def SearchItem(search_text, search_box = "Search products, articles & help topics", search_button_id = "ctl00_MasterPageHeader_GlobalSearchUC_BtnSubmitSearch"):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        time.sleep(5)
        #.// will allow us to look at only limited depth
        print "Searching for: %s" %search_text
        CommonUtil.ExecLog(sModuleInfo, "Searching for: %s" %search_text, 1)
        for elem in sBrowser.find_elements_by_xpath('//input[@title="%s"]'%search_box):
            print "Found the search box"
            CommonUtil.ExecLog(sModuleInfo, "Found the search box", 1)
            elem.send_keys(search_text) 
            print "Entered search item %s in the box"%search_box
            CommonUtil.ExecLog(sModuleInfo, "Entered search item %s in the box"%search_box, 1)
            search_button  = False
            search_button = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(search_button_id))
            if search_button != False:
                search_button.click()
                print "Successfully clicked the search item"
                CommonUtil.ExecLog(sModuleInfo, "Successfully clicked the search item", 1)
                try:
                    WebDriverWait(sBrowser, 30)
                except Exception, e:
                    print "Exception : ", e
                    CommonUtil.ExecLog(sModuleInfo, "Timed out waiting over 30 seconds for the page to load", 3)
                    print "Timed out waiting over 30 seconds for the page to load"
                    return "Critical"
                print "Waited for browser to load"
                CommonUtil.ExecLog(sModuleInfo, "Waited for browser to fully load: %s" %search_text, 1)
                return "PASS"
            else:
                print "Search button was not found"
                CommonUtil.ExecLog(sModuleInfo, "Search button was not found: %s" %search_text, 3)
                return "Critical"
        print "Unable to find search box"
        CommonUtil.ExecLog(sModuleInfo, "Unable to find search box: %s" %search_text, 3)
        return "Critical"
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Framework error with searching your item: %s" %search_text, 3)
        print "Framework error with searching your item: %s" %search_text
        return "Critical"

def GetItemDetail():
    '''
    This should be actually used during the verification.. Please do not add any loggign to this module
    '''
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    title_id = "ctl00_CC_ctl00_PD_lblProductTitle"
    model_number = "ctl00_CC_ctl00_PD_lblModelNumber"
    web_id = "ctl00_CC_ctl00_PD_lblSku"
    prod_sale_price = "prod-price sale"
    prod_saving = "prod-saving"
    sale_price_dollar = ""
    sale_dollar_cent = ""
    sale_price_cents = ""
    product_title= []
    product_model =[]
    prod_web_id =[]
    sale_price = []
    saving=[]
    details_specs = []
    full_product_detail = []
    
    time.sleep(3)
    try:
        prod_title = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(title_id))
        product_title.append("Title")
        product_title.append(prod_title.text)
        print "Successfully collected product title"
    except:
        print "Unable to collect product title" 
    try:
        prod_model_number = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(model_number))
        product_model.append("Model")
        product_model.append(prod_model_number.text)
        print "Successfully collected the model number"
    except:
        print "Unable to collect model number"
    try:
        prod_web_id_value = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(web_id))
        prod_web_id.append("Web ID")
        prod_web_id.append(prod_web_id_value.text)
        print "Successfully collected Web ID"   
    except:
        print "Unable to collect Web ID"    
    #sale price
    try:
        for elem in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//div[@class="%s"]'%prod_sale_price))):
            try:
                for price_dollars in sBrowser.find_elements_by_xpath('.//span[@class = "dollars"]'):
                    sale_price_dollar = price_dollars.text
                    print "Successfully collected sale price in dollars"
                    break
            except:
                print "Unable to collect sale price in dollars"
            try:
                for price_cents in sBrowser.find_elements_by_xpath('.//span[@class = "cents"]'):
                    sale_price_cents = price_cents.text  
                    print "Successfully collected sale price in cents"
                    break
            except:
                print "Unable to collect sale price for cents"
        sale_dollar_cent = sale_price_dollar+"."+sale_price_cents
        sale_price.append("Sale Price")
        sale_price.append(sale_dollar_cent)   
        print "Successfully collected sale price information" 
    except:
        print "Unable to collect Sale Price information"
    #saving  
    try: 
        for sale_ele in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//div[@class="%s"]'%prod_saving))):
            for price_dollars in sBrowser.find_elements_by_xpath(".//span[contains(text(),'$')]"):
                break
        saving.append("Saving")    
        saving.append(price_dollars.text)  
        print "Successfully collected saving price"
    except:
        print "Unable to collect saving price"
    #Selecting detail and specs of the product 
    try:
        menu_name_3 = "Details and Specs"    
        time.sleep(1)
        allElements= sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name_3))
        for eachElements in allElements:
            eachElements.click()
            break
    except:
        print "Error trying to select the Detail & Specs"
    try:
        time.sleep(1)  
        table_x = []
        table_y = []
        xpath = '//*[@class="span5"]'
        for i in sBrowser.find_elements_by_xpath(xpath):
            table_x.append(i.text)
        xpath = '//*[@class="span7"]'   
        for j in sBrowser.find_elements_by_xpath(xpath):
            table_y.append(j.text)
        for x, y in zip(table_x, table_y):
            total = x,y
            details_specs.append(total)
        print 'successfully collected all the detail and specs'
    except:
        print "Unable to collect detail and specs detail"
    full_product_detail.append(product_title)
    full_product_detail.append(product_model)
    full_product_detail.append(prod_web_id)
    full_product_detail.append(sale_price)
    full_product_detail.append(saving)
    full_product_detail.append(details_specs)
    return full_product_detail    
    
    
    

#print BrowserSelection('Firefox')
#print OpenLink('http://www.futureshop.ca')
#print SelectFirstLevelMenu ('Departments')
#print SelectSecondLevelMenu('Computers & Software')
#print SelectThirdLevelMenu('iPad & Tablets')
##print SelectThirdLevelMenu('Software')
#print FilterBySelection("On Sale")
#print GetFilterCount("On Sale")

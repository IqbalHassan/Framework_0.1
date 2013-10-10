'''
Created on Sep 22, 2013

@author: Riz
'''
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.selenium as Sal
import WebProgram
import time
import inspect
from selenium.webdriver.support.ui import WebDriverWait
import webdriverplus
from selenium.webdriver.common.action_chains import ActionChains
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
    try:
        if browser == 'Chrome':
            sBrowser = webdriver.Chrome()
            print "Started Chrome Browser"
            return "Passed"
        elif browser == 'Firefox':
            sBrowser = webdriver.Firefox()
            print "Started Firefox Browser"
            return "Passed"
        elif browser == 'IE':
            sBrowser = webdriver.Ie()
            print "Started Internet Explorer Browser"
            return "Passed"
        else:
            print "not a valid browser selection"
            return "Critical"
    except:
        print "Unable to start WebDriver"
        return "Critical"

def OpenLink(link):
    try:
        #WebDriverWait(sBrowser, 10)
        #WebDriverWait(sBrowser, 10).until(lambda driver : sBrowser.get(link))
        sBrowser.get(link)
        WebDriverWait(sBrowser, 30)
        #link_page.wait_for_page_to_load(1000)
        print "successfully opened browser: " +link
        return "Passed"
    except:
        print "unable to open browser: " + link 
        return "Critical"

def SelectFirstLevelMenu(menu_name_1):
    try:
        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements)== 0:
            print "Unable to find your main menu object"
            return "Critical"
        for element in allElements:
            if menu_name_1 == element.text:
                print "Found the Main Menu: " + element.text
                result = HoeverOver(element)
                if result != "Passed":
                    return "Critical"
                else: 
                    return "Passed" 
        print "Unable to find your element: " + menu_name_1
        return "Critical"
    except:
        print "Error trying to select the main menu"
        return "Critical"
        
                
def SelectSecondLevelMenu(menu_name_2):
    try:
        #menu_name_2 = "filter-"+ (check_box_name.replace(" ", "-")).lower()
        
        allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
        if len(allElements)== 0:
            print "Unable to find your main menu object"
            return "Critical"
        for element in allElements:
            if menu_name_2 == element.text:
                print "Found the Main Menu: " + element.text
                result = HoeverOver(element)
                if result != "Passed":
                    return "Critical"
                else: 
                    return "Passed" 
        print "Unable to find your element: " + menu_name_2
        return "Critical"
    except:
        print "Error trying to select the second level menu"
        return "Critical"

def SelectThirdLevelMenu(menu_name_3):
    try:
        allElements= sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name_3))
        for eachElements in allElements:            
            if  menu_name_3 == eachElements.get_attribute("text"):
                print "Found your selection: " +  menu_name_3              
                sBrowser.get(eachElements.get_attribute('href'))
                print "Successfully clicked your item: " + menu_name_3
                return "Passed"
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
        return "Passed"
    except:
        print "Unable to hover over the element"
        return "Critical"
        
def FilterBySelection(check_box_name):
    try:
        
        check_box = "filter-"+ (check_box_name.replace(" ", "-")).lower()
        #.// will allow us to look at only limited depth
        #WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_element_by_name(sValue))
        #all_elements = WebDriverWait(sBrowser, 5).until(lambda driver : sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%check_box))
       
        for elem in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%check_box))):
            print 'Your check box %s is found but it is currently not checked' %check_box_name
            for elem in sBrowser.find_elements_by_xpath('.//span[@class = "item"]'):
                if elem.text == check_box_name:
                    elem.click()
                    time.sleep(5)
                    print "Your check box: %s is now checked" %check_box_name
                    return "Passed"
        #Verify if check box was already checked
        if_check_box_checked = check_box + " is-selected"
        #for elem in sBrowser.find_elements_by_xpath('.//li[@class = "filter-on-sale is-selected"]'):
        for elem in sBrowser.find_elements_by_xpath('.//li[@class="%s"]'%if_check_box_checked):
            print "your check box was already selected"
            return "Passed"
        print "Unable to locate your check box: %s"  %check_box_name 
        return "Critical"
        
    except:
        print "Unable to select your check box: %s" %check_box_name


def RemoveFilter(check_box_name):
    print 'checkbox'            




def GetFilterCount(check_box_name):
    try:
        #Since checkbox name changes dynamically when you select, we need to first 
        #try to see if it works with unchecked name and then we will try with 
        #checked name
        unchecked_name = "filter-"+ (check_box_name.replace(" ", "-")).lower()
        checked_name  = unchecked_name + " is-selected"
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]'%unchecked_name)
        #check_box_name = check_box_name_count.find_element_by_xpath('.//span[@class="item"]')
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        #check_box_status = check_box_name_count.find_element_by_xpath('.//input[@type="checkbox"]')
        print "Found your checkbox and the count is: %s" %check_box_count.text
        replace1 =(check_box_count.text).replace("(", "")
        return replace1.replace(")","")
    except:
        print "Unable to find the check box.  It may be checked.  I will try to find if check box is checked"
    try:
        check_box_name_count = sBrowser.find_element_by_xpath('//li[@class="%s"]'%checked_name)
        #check_box_name = check_box_name_count.find_element_by_xpath('.//span[@class="item"]')
        check_box_count = check_box_name_count.find_element_by_xpath('.//span[@class="count"]')
        #check_box_status = check_box_name_count.find_element_by_xpath('.//input[@type="checkbox"]')
        print "Found your checkbox.  It was checked.  Your count is: %s" %check_box_count.text
        replace1 =(check_box_count.text).replace("(", "")
        return replace1.replace(")","")
    except:
        print "Unable to find the check box"
        return "Critical"
                    





def SearchItem(search_text, search_box = "Search products, articles & help topics", search_button_id = "ctl00_MasterPageHeader_GlobalSearchUC_BtnSubmitSearch"):
    try:
        time.sleep(5)
        #.// will allow us to look at only limited depth
        print "Searching for: %s" %search_text
        for elem in sBrowser.find_elements_by_xpath('//input[@title="%s"]'%search_box):
            print "Found the search box"
            elem.send_keys(search_text) 
            print "Entered search item in the box"  
            search_button  = False
            search_button = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(search_button_id))
            if search_button != False:
                search_button.click()
                print "Successfully clicked the search item"
                WebDriverWait(sBrowser, 30)
                print "Waited for browser to load"
                return "Passed"
            else:
                print "Search button was not found"
                return "Critical"
        print "Unable to find search box"
        return "Critical"
            
    except:
        print "Framework error with searching your item: %s" %search_text



def GetItemDetail():
    #this should be actually used during the verification.. shouldnt need 
    title_id = "ctl00_CC_ctl00_PD_lblProductTitle"
    model_number = "ctl00_CC_ctl00_PD_lblModelNumber"
    web_id = "ctl00_CC_ctl00_PD_lblSku"
    
    print BrowserSelection('Firefox')       
    print OpenLink('http://www.futureshop.ca/en-CA/product/samsung-samsung-37-1080p-60hz-led-hdtv-un37eh5000fxzc-un37eh5000fxzc/10251591.aspx?path=691d0fa30eadcbbdc746003f05b77732en02')
    prod_sale_price = "prod-price sale"
    prod_saving = "prod-saving"
    
    sale_price_dollar = ""
    
    prod_title = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(title_id))
    product_title = prod_title.text
    
    prod_model_number = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(model_number))
    print prod_model_number.text
    
    prod_web_id = WebDriverWait(sBrowser, 20).until(lambda driver : sBrowser.find_element_by_id(web_id))
    print prod_web_id.text
    
    
    #sale price
    for elem in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//div[@class="%s"]'%prod_sale_price))):
        print "the sale price is:"
        for price_dollars in sBrowser.find_elements_by_xpath('.//span[@class = "dollars"]'):
            sale_price_dollar = price_dollars.text
            print sale_price_dollar
        for price_cents in sBrowser.find_elements_by_xpath('.//span[@class = "cents"]'):
            sale_price_cents = price_cents.text  
            print  sale_price_cents
    
    #saving     
    for sale_ele in (WebDriverWait(sBrowser, 5).until(lambda driver: sBrowser.find_elements_by_xpath('.//div[@class="%s"]'%prod_saving))):
        print "Total saving is:"
        #print sale_ele
        for price_dollars in sBrowser.find_elements_by_xpath(".//span[contains(text(),'$')]"):
            #print price_dollars
            print price_dollars.text
            break
          
    menu_name_3 = "Details and Specs"    
    time.sleep(1)
    try:
        allElements= sBrowser.find_elements_by_xpath ("//*[contains(text(),'%s')]" % (menu_name_3))
        for eachElements in allElements:
            eachElements.click()
            break
    except:
        print "Error trying to select the main menu"
    
    time.sleep(1)  
    
    table_list = []
    
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
        table_list.append(total)
    
    
    
    print table_list
        
    
    #print i

#print BrowserSelection('Firefox')       
#print OpenLink('http://www.bestbuy.ca')
#SearchItem('10258650', search_button_id = "ctl00_MasterHeader_ctl00_uchead_GlobalSearchUC_BtnSubmitSearch")

#print BrowserSelection('Firefox')       
#print OpenLink('http://www.futureshop.ca')
#SearchItem('10258650')
#GetItemDetail()

#    
#print BrowserSelection('Chrome')       
#print OpenLink('http://www.futureshop.ca')    
#print SelectFirstLevelMenu ('Departments')          
#print SelectSecondLevelMenu('Appliances')
#print SelectThirdLevelMenu('Laundry Pairs')
##print SelectThirdLevelMenu('Software')
#print FilterBySelection("On Sale")
#print GetFilterCount("On Sale")
#
#
#
#






















'''

for elem in sBrowser.find_elements_by_xpath('.//span[@class = "item"]'):
    #print elem.text
    if elem.text == "On Sale":
        print elem.id
        print elem.is_selected()
        elem.click()
        time.sleep(5)
        break
for elem in sBrowser.find_elements_by_xpath('.//li[@class = "filter-on-sale"]'):
    print 'filter on sale check box is not chcked'
for elem in sBrowser.find_elements_by_xpath('.//li[@class = "filter-on-sale is-selected"]'):
    print 'filter on sale check box is chcked'    
'''

'''
#for this method we will need to use the data_path as attribute
allElements = sBrowser.find_elements_by_xpath("//input[@type='checkbox']")


for eachElements in allElements:
    print eachElements
#sBrowser.find_element_by_name('On Sale').is_selected()
'''

'''
#open a link without item being displayed
allElements = WebDriverWait(sBrowser, 45).until(lambda driver : sBrowser.find_elements_by_xpath("//*[@href]"))

for eachElements in allElements:
    href_value = eachElements.get_attribute('href')
    print href_value
    
    if  "ipad-tablets" in str(href_value):
        print href_value
        sBrowser.get(href_value)
        #eachElements.click()
        break 
'''

'''   
     #partial text and href:
     links = browser.find_elements_by_partial_link_text('##')
    for link in links:
        print link.get_attribute("href")
'''           

'''

#allElements = sBrowser.find_elements_by_xpath("//*[@href]")

for eachElements in allElements:
    title_value = eachElements.get_attribute('href')
    #print title_value
    if  "product" in str(title_value):
        print title_value
        break 
    
print eachElements
eachElements.click()


'''







''''
##sValue= "Search products, articles & help topics"
###
#allElements = sBrowser.find_elements_by_xpath("//*[@href]")
#allElements = sBrowser.find_elements_by_xpath(".//a[@class]")
#print len(allElements)
#for each in allElements:
#
#    if 'Departments' == each.text:
#        print "found the element"
#        #wd = webdriver_connection.connection
#        hov = ActionChains(sBrowser).move_to_element(each)
#        hov.perform()
#        
#    

'''





#Enter text in search field

#print  eachElements.get_attribute('id')
#
#eachElements.send_keys('computer')
#
#b = sBrowser.find_element_by_id("ctl00_MasterPageHeader_GlobalSearchUC_BtnSubmitSearch")
#b.click()
#search_box = sBrowser.find_element_by_id("ctl00_MasterPageHeader_GlobalSearchUC_Path")
#
#search_box.send_keys('fuck')

'''

!!!!For IE Support!!!!!                 
Please download IEDriver.exe from http://code.google.com/p/selenium/downloads/list
And IEDriver executable needs to be available in the path, same path where BES_Activation.py file is.                


Browser = ""


class Paths_Ids():
    #LOGIN
    MainUrl = "https://bbapp064qb03.bbapps.sqm.testnet.rim.net/webconsole/login"
    MainUrl2 = "https://tabds05-ssvv.sqm.testnet.rim.net/webconsole/appMain.html"
    FirstLoginLinkId = 'loginLink' 
    
    UserFieldId = 'text_username'
    UserName = "fumalik1e07" 
    #'testUserqb01'
    
    PasswordFieldId = 'text_password'
    Password = 'password'
    
    DomainFieldId = "text_domain"
    DomainValue = "bbapps.sqm.testnet.rim.net"
    
    
    DomainId = 'authenticatorPropertySelection'
    SecondLoginLinkId = 'link_login'
    
    #Attached device
    AttchedDeviceCssPath = 'a#linkToggle_NODE_ATTACHED_DEVICES img'
    #Manage Current Device
    ManageCurrentDeviceId = "NODE_ATTACHED_DEVICES"
    
    #Manage User
    ManageUserid = 'leftPageLink_0'
    
    #Search User
    InputUserFieldId = 'displayNameInputElse'
    SearchLinkId = 'searchLink'
    
    ManageCurrentDevice = "Manage current device"
    
    AssignCurrentDevice = 'Assign the current device to a user'


def BESLogin(BESAccountName = None, sPassword = None):
    
    #Browser=webdriver.Ie()
    Browser = webdriver.Firefox()
    Browser.get("https://bbapp064qb03.bbapps.sqm.testnet.rim.net/webdesktop/app")
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #Entering User Name
        
        UserName = WebProgram.FindElement(Browser,'id',Paths_Ids.UserFieldId)
        UserName.send_keys(BESAccountName)
        
        #Entering Password
        Password = WebProgram.FindElement(Browser,'id',Paths_Ids.PasswordFieldId)
        Password.send_keys(Paths_Ids.Password)
        
        #Entring Domain
        Domain = WebProgram.FindElement(Browser, 'id',Paths_Ids.DomainFieldId)
        Domain.send_keys(Paths_Ids.DomainValue)
        
        #Selecting "BlackBerry Administration Service" from drop down
    #    DropDown = Select(WebProgram.FindElement(Browser,'id',Paths_Ids.DomainId))
    #    DropDown.select_by_index(1)
        
        #Clicking Login Button
        LoginButton = WebProgram.FindElement(Browser,'id',Paths_Ids.SecondLoginLinkId)
        LoginButton.click()
        
        print "%s > Successfully logged in using user: '%s' " %(sModuleInfo,BESAccountName)
        CommonUtil.ExecLog(sModuleInfo,"Successfully logged in using user: '%s'" %BESAccountName,1)
        return Browser
    
    
    except Exception,e:
         Browser.close()
         return CommonUtil.LogCriticalException(sModuleInfo,e)    
    

def CreateActivationPassword(sEmailID = None, sEmailPassword = None ,sActivationPassword = "1111"):
    
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #if sEmailID == None: sEmailID = CommonUtil.GetLocalUser().lower()
        #if sEmailPassword == None: sEmailPassword = "password"
        #if sEmailID == None: sEmailID = Paths_Ids.UserName
        #if sEmailPassword == None: sEmailPassword = Paths_Ids.Password
        LocalUserid  = (CommonUtil.GetLocalUser()).lower()
        BESAccountName = LocalUserid
#        BESAccountName = "fumalik1e07"
        Browser = BESLogin(BESAccountName)
        if Browser == "Critical": return "Critical"
        time.sleep(3)
        Browser.switch_to_default_content()
        time.sleep(1)
        Browser.switch_to_frame("appFrame")
        time.sleep(1)
        Browser.switch_to_frame("mainFrame")  
        
        #Clicking 'Create Activation Password' link
        time.sleep(2)
        PasswordLink = WebProgram.FindElement(Browser,'link_text',"Create an Activation Password")
        if PasswordLink:
            print "Link found"
        else:
            print "%s > Create an Activation Password Link could not found " %sModuleInfo
            CommonUtil.ExecLog(sModuleInfo,"Create an Activation Password Link could not found",3)
            Browser.close()
            return "Critical"
        PasswordLink.click()
        
        #Entering Password
        ActivationPassword = WebProgram.FindElement(Browser,'id',"passwordInput")
        ActivationPassword.send_keys("1111")
        #Confirmation Password
        ConfirmActivationPassword = WebProgram.FindElement(Browser,'id',"confirmPasswordInput")
        ConfirmActivationPassword.send_keys("1111")
        
        #Clicking 'Set the activation password'
        time.sleep(1)
        Browser.switch_to_default_content()
        time.sleep(1)
        Browser.switch_to_frame("appFrame")
        time.sleep(1)
        Browser.switch_to_frame("mainFrame") 
        time.sleep(3)
        SetActivationPassword = WebProgram.FindElement(Browser,'link_text',"Set the activation password")
        if SetActivationPassword:
            print "Activation Password link found"
        else:
            print "%s > Set the activation password Link could not found " %sModuleInfo
            CommonUtil.ExecLog(sModuleInfo,"Set the activation password Link could not found" %BESAccountName,3)
            Browser.close()
            return "Critical"
        time.sleep(3)
        SetActivationPassword.click()
        
        print "%s > Password has been activated for '%s' " %(sModuleInfo,BESAccountName)
        CommonUtil.ExecLog(sModuleInfo,"Password has been activated for '%s'" %BESAccountName,1)
        Browser.close()
        return "Pass"
    
    except Exception,e:
         Browser.close()
         return CommonUtil.LogCriticalException(sModuleInfo,e)


def BESActivationProcess():

    
    BESLogin()
    
    time.sleep(3)
    Browser.switch_to_default_content()
    Browser.switch_to_frame("appFrame")
    Browser.switch_to_frame("treeFrame")  
    
    #Clicking Attached Device link
    AttachedDevice = WebProgram.FindElement(Browser,'css_selector',Paths_Ids.AttchedDeviceCssPath)
    AttachedDevice.click()
    time.sleep(20)
    #Clicking Manage current device link
    ManageCurrentDevice = WebProgram.FindElement(Browser,'id',Paths_Ids.ManageCurrentDeviceId)
    ManageCurrentDevice.click()
    
    #Clicking Manage current device
    CurrentDevice = WebProgram.FindElement(Browser,'link_text',Paths_Ids.ManageCurrentDevice)
    CurrentDevice.click()
    
    #Clicking Assign the current device to a user
    AssignDevice = WebProgram.FindElement(Browser,'link_text',Paths_Ids.AssignCurrentDevice)
    AssignDevice.click()
    
    
    #Switching to Frames
    Browser.switch_to_default_content()
    Browser.switch_to_frame("appFrame")
    Browser.switch_to_frame("mainFrame")  
    
    
    #Searching required user
    DisplayUserField = WebProgram.FindElement(Browser,'id',Paths_Ids.InputUserFieldId)
    DisplayUserField.send_keys(LocalUser)
    
    #Clicking search link
    SearchButton = WebProgram.FindElement(Browser,'id',Paths_Ids.SearchLinkId)
    SearchButton.click()
    
    #Clicking user name radio button from list, the list came after clicking search link
    UserName = WebProgram.FindElement(Browser,'id','userSelectionInputGroup0')
    UserName.click()

    
    #Clicking Associate user link
    AssociateUser = WebProgram.FindElement(Browser,'link_text','Associate user')
    AssociateUser.click()
    


    
#print BESLogin()



#print CreateActivvationPassword()
#print BESActivationProcess()
#    Browser.quit()


#print CreateActivationPassword()
'''
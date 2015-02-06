
import SeleniumScript

def start_browser(dependency,step_data):
    sClientName=dependency['Browser']
    sTestStepReturnStatus = SeleniumScript.BrowserSelection(sClientName)
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def go_to_a_weblink(dependency,step_data):
    first_data_set=step_data[0]
    web_link=first_data_set[0][2]
    title=first_data_set[0][2]
    sTestStepReturnStatus = SeleniumScript.OpenLink(web_link, title)
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def login(dependency,step_data):
    first_data_set=step_data[0]
    user_name = first_data_set[0][2]
    password = first_data_set[1][2]
    sTestStepReturnStatus = SeleniumScript.Login(user_name,password)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
    
def expand_menu_by_name_or_id(dependency,step_data):
    first_data_set=step_data[0]
    menu_name=first_data_set[0][2]
    sTestStepReturnStatus = SeleniumScript.Expand_Menu_By_Name_OR_ID(menu_name)
    print sTestStepReturnStatus
    return sTestStepReturnStatus       

def click_element_by_name_or_id(dependency,step_data):
    first_data_set=step_data[0]
    element_name=first_data_set[0][2]
    sTestStepReturnStatus = SeleniumScript.Click_Element_By_Name_OR_ID(element_name)
    print sTestStepReturnStatus
    return sTestStepReturnStatus  

def close_browser(dependency,step_data):
    sTestStepReturnStatus = SeleniumScript.CloseBrowser()
    print sTestStepReturnStatus
    return sTestStepReturnStatus

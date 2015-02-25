
import sys
sys.path.append("..")
from Web import SeleniumScript


def start_browser(dependency,step_data):
    try:
        sClientName=dependency['Browser']
        sClientName = sClientName.lower()
        sTestStepReturnStatus = SeleniumScript.BrowserSelection(sClientName)
        print sTestStepReturnStatus
        return sTestStepReturnStatus
    except:
        return "Failed"

def go_to_a_weblink(dependency,step_data):
    try:
        first_data_set=step_data[0]
        web_link=first_data_set[0][1]
        title=first_data_set[1][1]
        sTestStepReturnStatus = SeleniumScript.OpenLink(web_link, title)
        print sTestStepReturnStatus
        return sTestStepReturnStatus
    except:
        return "Failed"

def log_in_to_clicksafety(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        user_name = first_data_set[0][1]
        password = first_data_set[1][1]
        sTestStepReturnStatus = SeleniumScript.Login(user_name,password)
        print sTestStepReturnStatus
        return sTestStepReturnStatus
    except:
        return "Failed"
    
def expand_menu_by_name_or_id(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        menu_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Expand_Menu_By_Name_OR_ID(menu_name)
        print sTestStepReturnStatus
        return sTestStepReturnStatus       
    except:
        return "Failed"
    
def click_element_by_name_or_id(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        element_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Click_Element_By_Name_OR_ID(element_name)
        print sTestStepReturnStatus
        return sTestStepReturnStatus  
    except:
        return "Failed"

def course_settings_time_limit(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        id_minlimit=first_data_set[0][0]
        minlimit_value =first_data_set[0][1]
        id_dailylimit=first_data_set[1][0]
        dailylimit_value =first_data_set[1][1]
        id_submitbutton =first_data_set[2][1]  
        sTestStepReturnStatus = SeleniumScript.Course_Settings_Time_Limit(id_minlimit,minlimit_value,id_dailylimit,dailylimit_value,id_submitbutton)
        print sTestStepReturnStatus
        return sTestStepReturnStatus  
    except:
        return "Failed"
    
def verify_text_message_by_class(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        message=first_data_set[0][0]
        expected_text =first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Verify_Text_Message_By_Class(message,expected_text)
        print sTestStepReturnStatus
        return sTestStepReturnStatus 
    except:
        return "Failed"
    
def turn_editing_on_or_off(dependency,step_data):
    try:        
        first_data_set=step_data[0]
        on_off =first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Turn_Editing_On_OR_Off(on_off)
        print sTestStepReturnStatus
        return sTestStepReturnStatus 
    except:
        return "Failed"

def tear_down(dependency,step_data):
    try:        
        sTestStepReturnStatus = SeleniumScript.Tear_Down()
        print sTestStepReturnStatus
        return sTestStepReturnStatus
    except:
        return "Failed"
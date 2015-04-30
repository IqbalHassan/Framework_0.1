import sys
sys.path.append("..")
from Web import SeleniumScript
def cancel_step_test(dependency,step_data):
    return "cancelled"
def start_browser(dependency,step_data,temp_q):
    try:
        sClientName=dependency['Browser']
        sClientName = sClientName.lower()
        sTestStepReturnStatus = SeleniumScript.BrowserSelection(sClientName)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

def go_to_a_weblink(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        web_link=first_data_set[0][1]
        title=first_data_set[1][1]
        sTestStepReturnStatus = SeleniumScript.OpenLink(web_link, title)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

def log_in_to_clicksafety(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        user_name = first_data_set[0][1]
        password = first_data_set[1][1]
        logged_user = first_data_set[2][1]
        sTestStepReturnStatus = SeleniumScript.Login(user_name,password,logged_user)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
    
def expand_menu_by_name(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        menu_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Expand_Menu_By_Name(menu_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus       
    except:
        temp_q.put("Failed")
        return "Failed"

def expand_menu_by_id(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        menu_id=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Expand_Menu_By_ID(menu_id)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus       
    except:
        temp_q.put("Failed")
        return "Failed"
    
def click_element_by_name(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        element_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Click_Element_By_Name(element_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus  
    except:
        temp_q.put("Failed")
        return "Failed"

def click_element_by_id(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        element_id=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Click_Element_By_ID(element_id)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus  
    except:
        temp_q.put("Failed")
        return "Failed"

def course_settings_time_limit(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        id_minlimit=first_data_set[0][0]
        minlimit_value =first_data_set[0][1]
        id_dailylimit=first_data_set[1][0]
        dailylimit_value =first_data_set[1][1]
        id_submitbutton =first_data_set[2][1]  
        sTestStepReturnStatus = SeleniumScript.Course_Settings_Time_Limit(id_minlimit,minlimit_value,id_dailylimit,dailylimit_value,id_submitbutton)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus  
    except:
        temp_q.put("Failed")
        return "Failed"
    
def verify_text_message_by_class(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        message=first_data_set[0][0]
        expected_text =first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Verify_Text_Message_By_Class(message,expected_text)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus 
    except:
        temp_q.put("Failed")
        return "Failed"
    
def turn_editing_on_or_off(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        on_off =first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Turn_Editing_On_OR_Off(on_off)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus 
    except:
        temp_q.put("Failed")
        return "Failed"

def go_to_clicksafety_course_settings(dependency,step_data,temp_q):
    try:        
        sTestStepReturnStatus = SeleniumScript.ClickSafety_Course_Settings()
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus 
    except:
        temp_q.put("Failed")
        return "Failed"

def edit_course_from_course_settings(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        course_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Edit_Course_From_Course_Settings(course_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus       
    except:
        temp_q.put("Failed")
        return "Failed"

def delete_a_course(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        course_name=first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Delete_A_Course(course_name)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus       
    except:
        temp_q.put("Failed")
        return "Failed"

def verify_user_level_settings(dependency,step_data,temp_q):
    try:        
        first_data_set=step_data[0]
        user_type =first_data_set[0][1]
        sTestStepReturnStatus = SeleniumScript.Verify_User_Level_Settings(user_type)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus 
    except:
        temp_q.put("Failed")
        return "Failed"

def tear_down(dependency,step_data,temp_q):
    try:        
        sTestStepReturnStatus = SeleniumScript.Tear_Down()
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def create_a_new_course(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        full_name=first_data_set[0][1]
        short_name=first_data_set[1][1]
        course_id=first_data_set[2][1]
        cleanup =first_data_set[3][1]
        sTestStepReturnStatus = SeleniumScript.Create_A_New_Course(full_name, short_name, course_id, cleanup)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus    
    except:
        temp_q.put("Failed")
        return "Failed"
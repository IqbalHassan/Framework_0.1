__author__ = 'Raju'
from Web import SproutSupport

def start_browser(dependency,step_data,temp_q):
    try:
        sClientName=dependency['Browser']
        sClientName = sClientName.lower()
        sTestStepReturnStatus = SproutSupport.BrowserSelection(sClientName)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def go_to_webpage(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        web_link=first_data_set[0][1]
        #title=first_data_set[1][1]
        sTestStepReturnStatus = SproutSupport.OpenLink(web_link)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def log_in_to_sprout(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        user_name = first_data_set[0][1]
        password = first_data_set[1][1]
        logged_user = first_data_set[2][1]
        sTestStepReturnStatus = SproutSupport.Login(user_name,password,logged_user)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def tear_down(dependency,step_data,temp_q):
    try:
        sTestStepReturnStatus = SproutSupport.Tear_Down()
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"

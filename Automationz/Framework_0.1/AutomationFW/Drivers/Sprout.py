__author__ = 'Raju'
from AutomationFW.Web import SproutSupport
import unittest
from funkload.BenchRunner import BenchRunner
from funkload.FunkLoadTestCase import FunkLoadTestCase
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

def change_profile_detail(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        firstname = first_data_set[0][1]
        lastname = first_data_set[1][1]
        sTestStepReturnStatus = SproutSupport.ChangeProfileDetail(firstname=firstname,lastname=lastname)
        print sTestStepReturnStatus
        temp_q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    except:
        temp_q.put("Failed")
        return "Failed"
def create_new_group(dependency,step_data,temp_q):
    try:
        first_data_set=step_data[0]
        group_name = first_data_set[0][1]
        description = first_data_set[1][1]
        group_type= first_data_set[2][1]
        sTestStepReturnStatus = SproutSupport.CreateGroup(group_name,description,group_type)
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

class Sprout(FunkLoadTestCase):
    def performance_test_case(self):
        print "hello world"

from funkload.BenchRunner import parse_sys_args

def performance_test_case(argument_list):
    options, args, module_name = parse_sys_args(argument_list)
    klass, method = args[1].split('.')
    bench = BenchRunner(module_name, klass, method, options)
    return bench.run()

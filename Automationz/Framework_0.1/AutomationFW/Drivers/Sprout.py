__author__ = 'Raju'
import os
from AutomationFW.CoreFrameWork import FileUtilities
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
    def setUp(self):
        self.server_url=self.conf_get('main','url')
    def performance_test_case(self):
        server_url=self.server_url
        username=self.conf_get('performance_test_case','username')
        password=self.conf_get('performance_test_case','password')
        path=self.conf_get('performance_test_case','path')
        server_url= 'http://127.0.0.1:8000'
        res = self.get(server_url, description='Get url')
        self.assertEqual(res.code, 200)
        #self.assertEqual(res.body, "Hello World")
        res=self.get(server_url+'/Home/Login/', params={'username':username,'password':password})
        self.assertEqual(res.code, 200)
        res=self.get(server_url+'/Home'+path)
        print res.code

from funkload.BenchRunner import parse_sys_args, load_unittest
from AutomationFW.CoreFrameWork.ConfigFileGenerator import write_config_file
from funkload.utils import mmn_encode
def performance_test_case(dependency_list,steps_data,temp_q):
    argument_list=dependency_list[2:]
    options, args, module_name = parse_sys_args(argument_list)
    klass, method = args[1].split('.')
    full_file_name=dependency_list[0]
    #generate the config file from here
    default_configs={
        'bench':[('cycles','5:10:20:50'),('duration',10),('startup_delay',0.01),('sleep_time',0.01),('cycle_time',1),('log_to','console file'),('sleep_time_min',0),('sleep_time_max',0.5),('log_path','Log/funkload-bench.log'),('result_path','Result/funkload-bench.xml')],
        'main': [('title','Performance Test Case in '+klass),('description','This will run a Performance Test case in '+klass+ ' module'),('url','http://127.0.0.1:8000')]
    }
    write_config_file(full_file_name,method,dependency_list[1],steps_data,default_configs,klass)
    test = load_unittest(module_name, klass,mmn_encode(method, 0, 0, 0), options)
    bench = BenchRunner(module_name, klass, method, options)
    return bench.run()

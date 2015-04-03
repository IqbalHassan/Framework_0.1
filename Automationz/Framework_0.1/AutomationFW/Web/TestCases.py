import sys
sys.path.append("..")

'''
To Run this suite, you need to:
search: "CommonUtil."
replace: "#CommonUtil."  in the file SeleniumScript
and comment the import:
#from CoreFrameWork import CommonUtil
'''

from SeleniumScript import *


def Repurchase_the_course_when_the_final_exam_is_failed_for_third_time():
    #make your test cases by re-using same steps
    result = BrowserSelection('chrome')
    result = OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    result = Login('admin','R@1ndrops', 'Admin User')   
    result = Turn_Editing_On_OR_Off('on')
     
    result = ClickSafety_Course_Settings()
    if result == 'failed':
        return 'failed'     
    result = Edit_Course_From_Course_Settings("csdev-iqbal")
    if result == 'failed':
        return 'failed'    
    result = Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    if result == 'failed':
        return 'failed'     
    result = Verify_Text_Message_By_Class('message', 'Updated successfully')
    if result == 'failed':
        return 'failed'     
    Tear_Down()
    return 'Test Case Passed'

    
def Create_a_new_course(course, cleanup, from_begining):
    #make your test cases by re-using same steps
    print BrowserSelection('ie')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops')
    course_exists = Course_Exists(course)
    if course_exists == "PASSED":
        print "Course is already created"
        print "Delete the course and recreate"
        Delete_A_Course()
    
    print Click_Element_By_Name('Turn editing on')
    print Expand_Menu_By_Name('Site administration')
    print Expand_Menu_By_Name('Plugins')
    print Expand_Menu_By_Name('Local plugins')
    print Expand_Menu_By_Name('ClickSafety')
    print Click_Element_By_Name('Course settings')
    print Click_Element_By_Name('Edit')
    print Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    print Verify_Text_Message_By_Class('message', 'Updated successfully')
    print Tear_Down()

def delete_a_course_test_case(course_name):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops',"Admin User")
    print Turn_Editing_On_OR_Off('on')
    print Delete_A_Course(course_name)
    


def Test_Suite():
    delete_a_course_test_case("auto1")
    #add additional test cases
    #print Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()
#     j = 10
#     i = 0
#     while i != j:
#         print Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()
#         i = i +1 
    #delete_a_course()  

Test_Suite()

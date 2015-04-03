import sys
sys.path.append("..")

'''

'''

from SeleniumScript import *


def Repurchase_the_course_when_the_final_exam_is_failed_for_third_time():
    #make your test cases by re-using same steps
    print BrowserSelection('chrome')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops', 'Admin User')   
    print Turn_Editing_On_OR_Off('on')
     
    print ClickSafety_Course_Settings() 
    print Edit_Course_From_Course_Settings("csdev-iqbal")
    print Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    print Verify_Text_Message_By_Class('message', 'Updated successfully')    
    Tear_Down()


    
def Test_Case_Create_a_new_course(course, cleanup, from_begining):
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

def Test_Case_Delete_A_Course_Test_Case(course_name):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops',"Admin User")
    print Turn_Editing_On_OR_Off('on')
    print Delete_A_Course(course_name)
    

def Create_New_Test_Case(course_name,short_name,course_id,cleanup=False):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops', 'Admin User')   
    print Create_A_New_Course(course_name, short_name, course_id,cleanup)
    
def Test_Suite():
    #Test_Case_Delete_A_Course_Test_Case("auto1")
    Create_New_Test_Case("auto1","auto1","auto1","true")

Test_Suite()

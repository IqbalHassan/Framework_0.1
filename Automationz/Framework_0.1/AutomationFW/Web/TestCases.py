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


def Test_Case_Create_New_Course(course_name,short_name,course_id,cleanup=False):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops', 'Admin User')   
    print Create_A_New_Course(course_name, short_name, course_id,cleanup)

def Test_Case_Delete_A_Course_Test_Case(course_name):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops',"Admin User")
    print Turn_Editing_On_OR_Off('on')
    print Delete_A_Course(course_name)
    


def Test_Case_Create_A_New_Student(user_name, first_name, last_name, email_add, new_password,city, cleanup):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops', 'Admin User')
    print Turn_Editing_On_OR_Off('on')   
    print Create_A_New_Student(user_name, first_name, last_name, email_add, new_password,city, cleanup)   


def Test_Case_Delete_A_Student(first_name, email_add):
    print BrowserSelection('Firefox')
    print OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print Login('admin','R@1ndrops', 'Admin User')
    print Turn_Editing_On_OR_Off('on') 
    print Delete_A_Student(first_name, email_add)  
    
def Test_Suite():
    #Test_Case_Delete_A_Course_Test_Case("auto1")
    #Test_Case_Create_New_Course("auto1","auto1","auto1","true")
    #Test_Case_Create_A_New_Student(user_name="auto1", first_name="firstauto1", last_name="lastauto1", email_add="info@automationsolutionz.com", new_password="@utom@ti0nP@ssw0rd",city="Waterloo", cleanup="true")   
    Test_Case_Delete_A_Student(first_name="firstauto1",email_add="info@automationsolutionz.com")

Test_Suite()

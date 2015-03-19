import sys
sys.path.append("..")

'''
To Run this suite, you need to:
search: "CommonUtil."
replace: "#CommonUtil."  in the file SeleniumScript
and comment the import:
#from CoreFrameWork import CommonUtil
'''


from Web import SeleniumScript


def Repurchase_the_course_when_the_final_exam_is_failed_for_third_time():
    #make your test cases by re-using same steps
    result = SeleniumScript.BrowserSelection('chrome')
    if result == 'failed':
        return 'failed'
    result = SeleniumScript.OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    if result == 'failed':
        return 'failed'
    result = SeleniumScript.Login('admin','R@1ndrops', 'Admin User')
    if result == 'failed':
        return 'failed'    
    result = SeleniumScript.Turn_Editing_On_OR_Off('on')
    if result == 'failed':
        return 'failed'     
    result = SeleniumScript.ClickSafety_Course_Settings()
    if result == 'failed':
        return 'failed'     
    result = SeleniumScript.Edit_Course_From_Course_Settings("csdev-iqbal")
    if result == 'failed':
        return 'failed'    
    result = SeleniumScript.Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    if result == 'failed':
        return 'failed'     
    result = SeleniumScript.Verify_Text_Message_By_Class('message', 'Updated successfully')
    if result == 'failed':
        return 'failed'     
    SeleniumScript.Tear_Down()
    return 'Test Case Passed'

    
def Create_a_new_course(course, cleanup, from_begining):
    #make your test cases by re-using same steps
    print SeleniumScript.BrowserSelection('ie')
    print SeleniumScript.OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print SeleniumScript.Login('admin','R@1ndrops')
    course_exists = SeleniumScript.Course_Exists(course)
    if course_exists == "PASSED":
        print "Course is already created"
        print "Delete the course and recreate"
        delete_a_course()
    
    print SeleniumScript.Click_Element_By_Name('Turn editing on')
    print SeleniumScript.Expand_Menu_By_Name('Site administration')
    print SeleniumScript.Expand_Menu_By_Name('Plugins')
    print SeleniumScript.Expand_Menu_By_Name('Local plugins')
    print SeleniumScript.Expand_Menu_By_Name('ClickSafety')
    print SeleniumScript.Click_Element_By_Name('Course settings')
    print SeleniumScript.Click_Element_By_Name('Edit')
    print SeleniumScript.Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    print SeleniumScript.Verify_Text_Message_By_Class('message', 'Updated successfully')
    print SeleniumScript.Tear_Down()

def delete_a_course():
    print SeleniumScript.BrowserSelection('Firefox')
    print SeleniumScript.OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print SeleniumScript.Login('admin','R@1ndrops')
    print SeleniumScript.Turn_Editing_On_OR_Off('on')

    


def Test_Suite():
    #add additional test cases
    print Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()
#     j = 10
#     i = 0
#     while i != j:
#         print Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()
#         i = i +1 
    #delete_a_course()  

Test_Suite()

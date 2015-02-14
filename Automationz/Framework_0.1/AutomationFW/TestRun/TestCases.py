import sys
sys.path.append("..")
#from myapp import SomeObject


from Web import SeleniumScript



def Repurchase_the_course_when_the_final_exam_is_failed_for_third_time():
    #make your test cases by re-using same steps
    print SeleniumScript.BrowserSelection('Firefox')
    print SeleniumScript.OpenLink('http://csdev-iqbal.jbldev.com/moodle/','csdev-iqbal')
    print SeleniumScript.Login('admin','R@1ndrops')
    print SeleniumScript.Click_Element_By_Name_OR_ID('Turn editing on')
    print SeleniumScript.Expand_Menu_By_Name_OR_ID('Site administration')
    print SeleniumScript.Expand_Menu_By_Name_OR_ID('Plugins')
    print SeleniumScript.Expand_Menu_By_Name_OR_ID('Local plugins')
    print SeleniumScript.Expand_Menu_By_Name_OR_ID('ClickSafety')
    print SeleniumScript.Click_Element_By_Name_OR_ID('Course settings')
    print SeleniumScript.Click_Element_By_Name_OR_ID('Edit')
    print SeleniumScript.Course_Settings_Time_Limit('id_minlimit', '600','id_dailylimit', '500','id_submitbutton')
    print SeleniumScript.Verify_Text_Message_By_Class('message', 'Updated successfully')
    print SeleniumScript.Tear_Down()


def Test_Suite():
    #add additional test cases
    Repurchase_the_course_when_the_final_exam_is_failed_for_third_time()

Test_Suite()

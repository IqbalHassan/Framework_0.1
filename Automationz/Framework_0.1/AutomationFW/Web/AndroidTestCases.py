from appium import webdriver

def setup_phone_call():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '4.2'
    desired_caps['deviceName'] = 'F4AZCY05A885'
    desired_caps['app'] = 'E:\Workspace\\android\com.dexetra.dialer.apk'
    android_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
    return android_driver
def setup_phone_text():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '4.2'
    desired_caps['deviceName'] = 'F4AZCY05A885'
    desired_caps['app'] = 'E:\Workspace\\android\Messaging_4.4.2-35_35.apk'
    android_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
    return android_driver

def phone_call():
    driver=setup_phone_call()
    txt_btn=driver.find_element_by_id('com.dexetra.dialer:id/txt_login_skip_signin')
    txt_btn.click()
    done_btn=driver.find_element_by_id('android:id/button3')
    done_btn.click()
    dialup_but=driver.find_element_by_id('com.dexetra.dialer:id/button_dialpad')
    dialup_but.click()
    edt_txt=driver.find_element_by_id('com.dexetra.dialer:id/digits')
    edt_txt.send_keys('01684667279')
    submit_bt=driver.find_element_by_id('com.dexetra.dialer:id/dialButton')
    submit_bt.click()
def text_message():
    driver=setup_phone_text()
    print driver
    skip_button=driver.find_element_by_id('com.softcoil.mms:id/first_launch_leader_skip2')
    skip_button.click()
    #promo_button=driver.find_element_by_id('com.softcoil.mms:id/banner_sms_promo')
    #promo_button.click()
    #ok_button=driver.find_element_by_id('android:id/button1')
    #ok_button.click()
    new_button=driver.find_element_by_id('com.softcoil.mms:id/action_compose_new')
    new_button.click()
    receive_button=driver.find_element_by_id('com.softcoil.mms:id/recipients_editor')
    receive_button.send_keys('01925348037')
    edit_button=driver.find_element_by_id('com.softcoil.mms:id/embedded_text_editor')
    edit_button.send_keys('Surprise Brother, Are you all right?')
    send_button=driver.find_element_by_id('com.softcoil.mms:id/send_button_sms')
    send_button.click()
def main():
    #phone_call()
    text_message()
if __name__=='__main__':
    main()
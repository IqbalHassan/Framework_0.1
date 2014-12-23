import datetime
import DataBaseUtilities as DBUtil
import FileUtilities as FileUtil
import Global
import CommonUtil
import Cleanup
import sys, os, time, inspect
import WebProgram
import itertools, operator
import Compare
#Ver1.0
#declaring the current module instance

current_module=sys.modules[__name__]

if os.name == 'nt':
    import clr, System
    clr.AddReference('UIAutomationClient')
    clr.AddReference('UIAutomationTypes')
    clr.AddReference('System.Windows.Forms')
    from System.Threading import Thread
    from System.Windows.Forms import SendKeys
    from System.Windows.Automation import *
    import Program as AutoUtil
    import WinCommonFoldersPaths as WinCom

if os.name == 'posix':
    import MacCommonFoldersPaths as ComPath
    import Program_Mac as PIM

"""
def open_browser(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    CommonUtil.ExecLog(sModuleInfo, "Opening browser", 1)
    browser = sClientName
    #Adding working around for the current bug where we are not able to select browser
    #browser = "Firefox"
    sTestStepReturnStatus = WebProgram.BrowserSelection(browser)
    print sTestStepReturnStatus
    return sTestStepReturnStatus


def go_to_webpage(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    web_link = DataSet[0][2]
    sTestStepReturnStatus = WebProgram.OpenLink(web_link)
    print sTestStepReturnStatus
    return sTestStepReturnStatus


def close_browser(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    CommonUtil.ExecLog(sModuleInfo, "skipping closing browser", 1)
    sTestStepReturnStatus = WebProgram.CloseBrowser()
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def open_futureshop(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    CommonUtil.ExecLog(sModuleInfo, "Opening futureshop site", 1)
    link = "http://www.futureshop.ca"
    sTestStepReturnStatus = WebProgram.OpenLink(link)
    sTestStepReturnStatus = "Passed"
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def select_main_menu(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    menu_name = DataSet[0][2]
    sTestStepReturnStatus = WebProgram.SelectFirstLevelMenu(menu_name)
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def select_sub_menu_one(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    menu_name = DataSet[0][2]
    sTestStepReturnStatus = WebProgram.SelectSecondLevelMenu(menu_name)
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def select_sub_menu_two(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    menu_name = DataSet[0][2]
    sTestStepReturnStatus = WebProgram.SelectThirdLevelMenu(menu_name)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
def select_filter_checkbox(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    for eachData in DataSet:
        check_box_name = eachData[2]
        sTestStepReturnStatus = WebProgram.FilterBySelection(check_box_name)
        if sTestStepReturnStatus != "Passed":
            return sTestStepReturnStatus
        print sTestStepReturnStatus
        return sTestStepReturnStatus
def search_for_an_item(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery):    
    DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
    search_text = DataSet[0][2]
    sTestStepReturnStatus = WebProgram.SearchItem(search_text)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
"""

def open_browser(run_id,dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    print dependency
    print step_data
    print run_id
    query="select rundescription from test_run_env where run_id='%s'"%run_id
    conn=DBUtil.ConnectToDataBase()
    rundescription=DBUtil.GetData(conn,query)
    conn.close()
    
    #fetch the browser_list:
    for each in dependency:
        if each[0]=='Browser':
            browser_list=each[1]
            break
    if isinstance(browser_list,list):    
        if isinstance(rundescription,list) and len(rundescription)==1:
            rundescription=rundescription[0]
            rundescription=rundescription.split(' ')
            print rundescription
            for each in rundescription:
                if each in browser_list:
                    sClientName=each
                    break
            CommonUtil.ExecLog(sModuleInfo, "Opening browser", 1)
            sTestStepReturnStatus = WebProgram.BrowserSelection(sClientName)
            print sTestStepReturnStatus
        else:
            sTestStepReturnStatus='Failed'
    else:
        sTestStepReturnStatus='Failed'
    return sTestStepReturnStatus
def ExecuteTestSteps(run_id,CurrentStep,q,dependency_list,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        print run_id
        print dependency_list
        print step_data
        #convert the current step into taking the string
        function_name=CurrentStep.lower().replace(' ','_')
        functionTocall=getattr(current_module, function_name)
        sTestStepReturnStatus=functionTocall(run_id,dependency_list,step_data)
    
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        sTestStepReturnStatus = "Failed"

    #Put the return value into Queue to send it back to main thread
    q.put(sTestStepReturnStatus)
    return sTestStepReturnStatus
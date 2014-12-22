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

#function for the query write
#get the add_find_sql_query

function_mappings={
    'Open Browser':open_browser,
    'Go to webpage':go_to_webpage,
    'Close Browser':close_browser,
    'Open Futureshop':open_futureshop,
    'Select Main Menu':select_main_menu,
    'Select Sub Menu 1':select_sub_menu_one,
    'Select Sub Menu 2':select_sub_menu_two,
    'Select Filter Checkbox':select_filter_checkbox,
    'Search For An Item':search_for_an_item
    #'Verify Filter Items Count':
    #'Verify Product Details': 
}

def get_add_find_SQLQuery(TCID,StepSeq,DataSet,referred_run):
    add_find_SQLQuery=("select pmd.id,pmd.field,pmd.value"
                " from result_test_cases tc,result_test_case_datasets tcd,result_test_steps_data tsd,result_container_type_data ctd,result_master_data pmd"
                " where tc.run_id=tcd.run_id"
                " and tc.tc_id=tcd.tc_id"
                " and tcd.run_id=tsd.run_id"
                " and tcd.tcdatasetid=tsd.tcdatasetid"
                " and tsd.testdatasetid=ctd.dataid"
                " and tsd.run_id=ctd.run_id"
                " and ctd.curname=pmd.id"
                " and ctd.run_id=pmd.run_id"
                " and tc.tc_id='%s'"
                " and tcd.tcdatasetid='%s'"
                " and tsd.teststepseq=%d"
                " and tc.run_id='%s' order by pmd.id"% (TCID,DataSet, StepSeq, referred_run))
    return add_find_SQLQuery

def get_edit_SQLQuery(TCID,StepSeq,Dataset,referred_run):
    edit_SQLQuery = ("select "
            " ctd.curname,"
            " ctd.newname"
            " from result_Test_Steps tst, result_test_case_datasets tcd, result_test_steps_data tsd, result_container_type_data ctd"
            " where"
            " tst.tc_id = tcd.tc_id"
            " and tst.run_id=tcd.run_id"
            " and tcd.tcdatasetid = tsd.tcdatasetid"
            " and tcd.run_id=tsd.run_id"
            " and tst.teststepsequence = tsd.teststepseq"
            " and tst.run_id=tsd.run_id"
            " and tsd.testdatasetid = ctd.dataid"
            " and tsd.run_id=ctd.run_id"
            " and tst.tc_id = '%s'"
            " and tst.teststepsequence = '%s'"
            " and tcd.tcdatasetid = '%s'"
            " and tst.run_id='%s'" % (TCID, StepSeq, Dataset,referred_run))
    return edit_SQLQuery    
"""
def ExecuteTestSteps(CurrentStep,  q,dependency_list,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        #add_find_SQLQuery=get_add_find_SQLQuery(TCID, StepSeq, DataSet,run_id)
        #edit_SQLQuery=get_edit_SQLQuery(TCID, StepSeq, DataSet,run_id)
        for each in function_mappings.keys():
            if CurrentStep==each:
                function_name=function_mappings[each]
                #things needed to generalize
                sTestStepReturnStatus=function_name(conn,sModuleInfo,sClientName,add_find_SQLQuery,edit_SQLQuery)
                break
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        sTestStepReturnStatus = "Failed"

    #Put the return value into Queue to send it back to main thread
    q.put(sTestStepReturnStatus)
    return sTestStepReturnStatus
"""


def ExecuteTestSteps(CurrentStep,q,dependency_list,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        print dependency_list
        print step_data
        sTestStepReturnStatus='Failed'
    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        sTestStepReturnStatus = "Failed"

    #Put the return value into Queue to send it back to main thread
    q.put(sTestStepReturnStatus)
    return sTestStepReturnStatus
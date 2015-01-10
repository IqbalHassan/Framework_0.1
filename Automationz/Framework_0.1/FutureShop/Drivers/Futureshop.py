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
import CompareModule

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

#lost steps
exp_SQLQuery = ("select  pmd.md_id, pmd.field, pmd.value from test_case_datasets tcd, expected_datasets ed, expected_container ec, container_type_data ctd, master_data pmd where tcd.tcdatasetid = ed.datasetid"
        " and ed.expectedrefid = ec.exprefid"
        " and ec.container_name = ctd.dataid"
        " and ctd.curname = pmd.id"
        " and ed.stepsseq = '%s'"
        " and tcd.tcdatasetid = '%s' order by pmd.id;" % (StepSeq, DataSet))
        
elif CurrentStep == "Verify Filter Items Count":
            DataSet = DBUtil.GetData(conn, exp_SQLQuery, False)
            check_box_name = DataSet[0][1]
            ExpDataList = [[(DataSet[0][1],DataSet[0][2])]]
            ActDataList = [[(check_box_name,WebProgram.GetFilterCount(check_box_name))]]

            objCompare = Compare.Compare()
            retValue = objCompare.FieldCompare(ExpDataList, ActDataList, [], [])
            if retValue == "Pass":
                sTestStepReturnStatus = "Pass"
            else:
                sTestStepReturnStatus = "Critical"

        elif CurrentStep == "Verify Product Details":
            DataSet = DBUtil.GetData(conn, exp_SQLQuery, False)
            DataGroup = []
            DataList = []
            ExpDataList = []
            ActDataList = []
            #Get expected data
            for key, group in itertools.groupby(DataSet, operator.itemgetter(0)):
                DataGroup.append(list(group))
            for eachGroup in DataGroup:
                DataList = [tuple(x[1:3])for x in eachGroup]
                #Replace address data id with actual data
                ExpAddrList = []
                for i in range(len(DataList) - 1, -1, -1):
                    eachData = DataList[i]
                    if eachData[1].startswith(x[0]):# == 'Details':
                        temp = list(DataList[i])
                        address_find_SQLQuery = ("select "
                        " pmd.field,"
                        " pmd.value"
                        " from master_data pmd"
                        " where"
                        " pmd.md_id = '%s'"
                        " ;" % (temp[1]))
                        AddressData = DBUtil.GetData(conn, address_find_SQLQuery, False)
                        temp[1] = AddressData
                        ExpAddrList.append(tuple(temp))
                        DataList.pop(i)
                for eachData in ExpAddrList:
                    DataList.append(eachData)
                ExpDataList.append(DataList)

            #Get actual data
            ActDataList = []
            ActItemDetail = WebProgram.GetItemDetail()
            if ActItemDetail == "Critical":
                CommonUtil.ExecLog(sModuleInfo, "Error in getting Product Details", 3)
                sTestStepReturnStatus = "Critical"
            else:
                ActDataList.append(ActItemDetail)
                objCompare = Compare.Compare()
                retValue = objCompare.FieldCompare(ExpDataList, ActDataList, [], ['Web ID'])
                if retValue == "Pass":
                    sTestStepReturnStatus = "Pass"
                else:
                    sTestStepReturnStatus = "Critical"


        else:
            sTestStepReturnStatus = "Warning"
            print "Unknown test step : ", CurrentStep
            CommonUtil.ExecLog(sModuleInfo, "Unknown test step : %s" % CurrentStep , 2)

    except Exception, e:
        print "Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        sTestStepReturnStatus = "Critical"

"""

def open_browser(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    CommonUtil.ExecLog(sModuleInfo, "Opening browser", 1)
    sClientName=dependency['Browser']
    sTestStepReturnStatus = WebProgram.BrowserSelection(sClientName)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
def go_to_webpage(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    #getting the first data set by this following lines
    first_data_set=step_data[0]
    web_link=first_data_set[0][2]
    sTestStepReturnStatus = WebProgram.OpenLink(web_link)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
def verify_product_details(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    expected_data=[]
    actual_data=[]
    #declaring the object compare
    oCompare=CompareModule.CompareModule()
    sTestStepReturnStatus=oCompare.FieldCompare(expected_data,actual_data)
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def count_shoe_size(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    for i in range(len(step_data)):
        CommonUtil.ExecLog(sModuleInfo, "Processing Dataset #%s" % (i + 1), 5)                
        expected_data=step_data[i]
        #search for the size for now.
        for each in expected_data:
            if each[0]=='size':
                size=each[2]
                break
        actual_data=WebProgram.getShoeCount(size)
        print actual_data
        oCompare=CompareModule.CompareModule()
        sTestStepReturnStatus=oCompare.FieldCompare(expected_data,actual_data)
        print sTestStepReturnStatus
        if sTestStepReturnStatus!="Passed":
            CommonUtil.ExecLog(sModuleInfo, "Expected data and actual data not match for Dataset #%s" % (i + 1), 3)
            break
    return sTestStepReturnStatus
def close_browser(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name    
    CommonUtil.ExecLog(sModuleInfo, "skipping closing browser", 1)
    sTestStepReturnStatus = WebProgram.CloseBrowser()
    print sTestStepReturnStatus
    return sTestStepReturnStatus
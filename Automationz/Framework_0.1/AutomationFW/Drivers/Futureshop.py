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
    from PCDesktop import Program as AutoUtil
    import WinCommonFoldersPaths as WinCom

if os.name == 'posix':
    import MacCommonFoldersPaths as ComPath
    from MacDesktop import Program_Mac as PIM

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
def search_for_an_item(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    first_data_set=step_data[0]
    search_text=first_data_set[0][2]
    sTestStepReturnStatus = WebProgram.SearchItem(search_text)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
def verify_product_details(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    actual_data=WebProgram.GetItemDetail()
    expected_data=step_data
    #making data compatible with the current format
    final_list=[]
    for each in actual_data:
        if isinstance(each[1],list):
            for eachitem in each[1]:
                final_list.append((each[0],eachitem[0],eachitem[1],False,False))
        else:
            final_list.append((each[0],'',each[1],False,False))
    
    #declaring the object compare
    oCompare=CompareModule.CompareModule()
    sTestStepReturnStatus=oCompare.compare(expected_data,[final_list])
    print sTestStepReturnStatus
    return sTestStepReturnStatus

def close_browser(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name    
    CommonUtil.ExecLog(sModuleInfo, "skipping closing browser", 1)
    sTestStepReturnStatus = WebProgram.CloseBrowser()
    print sTestStepReturnStatus
    return sTestStepReturnStatus
def verifying_contacts(dependency,step_data):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name    
    expected_list=step_data
    actual_list=[ 
                 [ ( 'name' , '' , 'saad' , True , False ) , ( 'roll' , '' , '0905012' , False , False ) ] , 
                 [ ( 'name' , '' , 'shetu' , True , False ) , ( 'roll' , '' , '0905011' , False , False ) , ( 'cg' , '' , '3.51' , False , False ) ] , 
                 [ ( 'name' , '' , 'minar' , True , False ) , ( 'roll' , '' , '0905105' , False , False ) ],
                 [ ( 'name' , '' , 'Saurov' , True , False ) , ( 'roll' , '' , '0905110' , False , False ) ],
                 [ ( 'name' , '' , 'System' , False , False ) , ( 'roll' , '' , '0905189' , False , False ),('address','home','jessore',False,False),('address','road',701,False,False)  ] ,
                 [ ( 'name' , '' , 'minar' , True , False ) , ( 'roll' , '' , '0905105' , False , False ),('address','home','jessore',False,False),('address','road',701,False,False) ],                 
                 ]
    keyfield_list=['name']
    oCompare=CompareModule.CompareModule()
    sTestStepReturnStatus=oCompare.compare(expected_list,actual_list,keyfield_list)
    print sTestStepReturnStatus
    return sTestStepReturnStatus
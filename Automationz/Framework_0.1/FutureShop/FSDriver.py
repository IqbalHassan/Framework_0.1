import datetime
import DataBaseUtilities as DBUtil
import FileUtilities as FileUtil
import Global
import CommonUtil
import Cleanup
import sys, os, time, inspect
import WebProgram

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


def ExecuteTestSteps(conn, CurrentStep, TCID, sClientName, StepSeq, DataSet, q):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:

        add_find_SQLQuery = ("select "
        " pmd.id,"
        " pmd.field,"
        " pmd.value"
        " from Test_Steps tst, test_case_datasets tcd, test_steps_data tsd, container_type_data ctd, master_data pmd"
        " where"
        " tst.tc_id = tcd.tc_id"
        " and tcd.tcdatasetid = tsd.tcdatasetid"
        " and tst.teststepsequence = tsd.teststepseq"
        " and tsd.testdatasetid = ctd.dataid"
        " and ctd.curname = pmd.id"
        " and tst.tc_id = '%s'"
        " and tst.teststepsequence = '%s'"
        " and tcd.tcdatasetid = '%s' order by pmd.id;" % (TCID, StepSeq, DataSet))

        edit_SQLQuery = ("select "
        " ctd.curname,"
        " ctd.newname"
        " from Test_Steps tst, test_case_datasets tcd, test_steps_data tsd, container_type_data ctd"
        " where"
        " tst.tc_id = tcd.tc_id"
        " and tcd.tcdatasetid = tsd.tcdatasetid"
        " and tst.teststepsequence = tsd.teststepseq"
        " and tsd.testdatasetid = ctd.dataid"
        " and tst.tc_id = '%s'"
        " and tst.teststepsequence = '%s'"
        " and tcd.tcdatasetid = '%s';" % (TCID, StepSeq, DataSet))

        exp_SQLQuery = ("select "
        " pmd.id,"
        " pmd.field,"
        " pmd.value"
        " from test_case_datasets tcd, expected_datasets ed, expected_container ec, container_type_data ctd, master_data pmd"
        " where"
        " tcd.tcdatasetid = ed.datasetid"
        " and ed.expectedrefid = ec.exprefid"
        " and ec.container_name = ctd.dataid"
        " and ctd.curname = pmd.id"
        " and ed.stepsseq = '%s'"
        " and tcd.tcdatasetid = '%s' order by pmd.id;" % (StepSeq, DataSet))

        exp_PerfQuery = ("select "
        " ec.container_name"
        " from test_case_datasets tcd, expected_datasets ed, expected_container ec"
        " where"
        " tcd.tcdatasetid = ed.datasetid"
        " and ed.expectedrefid = ec.exprefid"
        " and ed.stepsseq = '%s'"
        " and tcd.tcdatasetid = '%s';" % (StepSeq, DataSet))


        if CurrentStep == "Open Browser":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            link = DataSet[0][0]
            sTestStepReturnStatus = WebProgram.BrowserSelection('Firefox')

        elif CurrentStep == "Open Futureshop":
            print "trying to print sbrower"
            
            link = "http://www.futureshop.ca"
            sTestStepReturnStatus = WebProgram.OpenLink(link)

        elif CurrentStep == "Select Main Menu":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            menu_name = DataSet[0][2]
            sTestStepReturnStatus = WebProgram.SelectFirstLevelMenu(menu_name)

        elif CurrentStep == "Select Sub Menu 1":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            menu_name = DataSet[0][2]
            sTestStepReturnStatus = WebProgram.SelectSecondLevelMenu(menu_name)

        elif CurrentStep == "Select Sub Menu 2":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            menu_name = DataSet[0][2]
            sTestStepReturnStatus = WebProgram.SelectThirdLevelMenu(menu_name)

        elif CurrentStep == "Select Filter Checkbox":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            for eachData in DataSet:
                check_box_name = eachData[2]
                sTestStepReturnStatus = WebProgram.FilterBySelection(check_box_name)
                if sTestStepReturnStatus != "Pass":
                    return sTestStepReturnStatus

        elif CurrentStep == "Verify Filter Items Count":
            DataSet = DBUtil.GetData(conn, add_find_SQLQuery, False)
            check_box_name = DataSet[0][1]
            exp_count = DataSet[0][2]
            if exp_count == WebProgram.GetFilterCount(check_box_name):
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

    #Put the return value into Queue to send it back to main thread
    q.put(sTestStepReturnStatus)
    return sTestStepReturnStatus


# -*- coding: cp1252 -*-
import os
import sys
from ConfigParser import DuplicateSectionError
import requests
from poster.streaminghttp import register_openers
import urllib2
from poster.encode import multipart_encode
import traceback, os.path
sys.path.append("..")
#adding driver folder to sys.path
current_file_path=os.path.dirname(os.getcwd())#getting parent folder
driver_folder=os.path.join(current_file_path,'Drivers')
if driver_folder not in sys.path:
    sys.path.append(driver_folder)
import ConfigParser
import time, datetime
import threading, Queue
import inspect
import DataBaseUtilities as DBUtil
import FileUtilities as FL
import CommonUtil
import Drivers
import importlib
import Global
import EmailNotify


#import FSDriver
from CoreFrameWork import Performance
#from distutils.tests.test_check import CheckTestCase
from CoreFrameWork import DataFetching
ReRunTag="ReRun"

passed_tag_list=['Pass','pass','PASS','PASSED','Passed','passed','true','TRUE','True',True,1,'1','Success','success','SUCCESS']
failed_tag_list=['Fail','fail','FAIL','Failed','failed','FAILED','false','False','FALSE',False,0,'0']

if os.name == 'nt':
    location = "X:\\Actions\\Common Tasks\\PythonScripts\\"
    if location not in sys.path:
        sys.path.append(location)
    current_location=os.getcwd()
    current_location=current_location+('\\Drivers\\')
    if current_location not in sys.path:
        sys.path.append(current_location)
def GetAllDriver():
    query="select distinct driver from test_steps_list"
    Conn=DBUtil.ConnectToDataBase()
    driver_name=DBUtil.GetData(Conn,query)
    driver_name.remove('Manual')
    return driver_name
def collectAlldependency(project,team):
    query="select dependency_name, array_agg(distinct name) from dependency d,dependency_management dm,dependency_name dn where d.id=dm.dependency and d.id=dn.dependency_id and dm.project_id='%s' and dm.team_id=%d group by dependency_name"%(project,int(team))
    conn=DBUtil.ConnectToDataBase()
    dependency_list=DBUtil.GetData(conn,query,False)
    conn.close()
    return dependency_list
def update_global_config(section,key,value):
    file_name=os.getcwd()+os.sep+'global_config.ini'
    config=ConfigParser.SafeConfigParser()
    config.read(file_name)
    temp=config.sections()
    list_item=[]
    for each in temp:
        temp_dict=dict(config.items(each))
        if key.lower() in temp_dict.keys():
            #update the key
            temp_dict[key.lower()]=value
        else:
            temp_dict.update({key.lower():value})
        list_item.append((each,temp_dict))
    print list_item
    for each in list_item:
        section=each[0]
        temp_dict=each[1]
        if not config.has_section(section):
            config.add_section(section)
        for eachitem in temp_dict.keys():
            config.set(section,eachitem,temp_dict[eachitem])
            
    with(open(file_name,'w')) as open_file:
        config.write(open_file)
                    
def main():
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    def TimeStamp():
        """

        ========= Instruction: ============

        Function Description:
        This function is used to create a Time Stamp for each test run.
        It will return current YearMonthDayHourMinuteSecond all in one string.
        This will be used to keep track of individual test run


        Parameter Description:
        - There are no parameter for this this function

        Example:
        - TimeStamp = TimeStamp()

        ======= End of Instruction: =========

        """
        now = datetime.datetime.now()
        year = "%d" % now.year
        month = "%d" % now.month
        day = "%d" % now.day
        hour = "%d" % now.hour
        minute = "%d" % now.minute
        second = "%d" % now.second
        Time_Stamp = year + month + day + hour + minute + second
        return Time_Stamp

    def ExecuteTestSteps(CurrentStep, TCID, sClientName, StepSeq, DataSet, sDeviceStorageType, q):
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        try:
            sTestStepReturnStatus = "Warning"
            print "Unknown test step : ", CurrentStep
            CommonUtil.ExecLog(sModuleInfo, "Unknown test step : %s" % CurrentStep , 2)
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()        
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
            print Error_Detail
            return CommonUtil.LogFailedException(sModuleInfo, Error_Detail)

        #Put the return value into Queue to send it back to main thread
        q.put(sTestStepReturnStatus)
        return sTestStepReturnStatus
    #End of ExecuteTestSteps Module

#*****************Start of Main Driver***************** 
    #connect db based on test case number get all test step

    # Here we are starting the main driver operations

#*****************Start of Main Driver***************** 
    #connect db based on test case number get all test step

    # Here we are starting the main driver operations

    """try:
        conn = DBUtil.ConnectToDataBase()
    except Exception, e:
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        #print "unable to connect to the database"
    CommonUtil.ExecLog(sModuleInfo, "Database connection successful" , 1)
    cur = conn.cursor()"""
    #first setup the config.ini file
    update_global_config('sectionOne','sTestStepExecLogId', sModuleInfo)
    conn=DBUtil.ConnectToDataBase()
    Userid = (CommonUtil.GetLocalUser()).lower()
    UserList = DBUtil.GetData(conn, "Select User_Names from permitted_user_list")
    conn.close()
    if Userid not in UserList:
        CommonUtil.ExecLog(sModuleInfo, "User don't have permission to run the tests" , 3)
        return "You Don't Have Permission"
    
    #Get all the drivers
    Driver_list=GetAllDriver()
    #Find Test Runs scheduled for this user from test_run_env table
    conn=DBUtil.ConnectToDataBase()
    TestRunLists = DBUtil.GetData(conn, "Select run_id,rundescription,tester_id from test_run_env Where tester_id = '%s' and (status = 'Submitted')" % Userid, False)
    conn.close()
    if len(TestRunLists) > 0:
        print "Running Test cases from Test Set : ", TestRunLists[0:len(TestRunLists)]
        CommonUtil.ExecLog(sModuleInfo, "Running Test cases from Test Set : %s" % TestRunLists[0:len(TestRunLists)], 1)
        
    else:
        print "No Test Run Schedule found for the current user :", Userid
        CommonUtil.ExecLog(sModuleInfo, "No Test Run Schedule found for the current user : %s" % Userid, 2)
        return False

    #Loop thru all the test runs scheduled for this user
    for TestRunID in TestRunLists:
        #get the dependency of all projects
        query="select distinct project_id, team_id from test_run_env tre, machine_project_map mpm where mpm.machine_serial=tre.id and run_id='%s'"%TestRunID[0]
        conn=DBUtil.ConnectToDataBase()
        project_team=DBUtil.GetData(conn,query,False)
        conn.close()
        dependency_list=collectAlldependency(project_team[0][0],project_team[0][1])
        #code for the dependency_list will go here.
        query="select rundescription from test_run_env where run_id='%s'"%TestRunID[0]
        conn=DBUtil.ConnectToDataBase()
        rundescription=DBUtil.GetData(conn,query)
        conn.close()
        dependency_list_final={}
        if isinstance(rundescription,list) and len(rundescription)==1:
            rundescription=rundescription[0]
            rundescription=rundescription.split(" ")
            for each in rundescription:
                for eachitem in dependency_list:
                    current_dependency=eachitem[0]
                    for eachitemlist in eachitem[1]:
                        if each==eachitemlist:
                            current_item=each
                            dependency_list_final.update({current_dependency:current_item})
        print dependency_list_final
        #TestResultsEnv Table
        #Update test_run_env table with status for the current TestRunId
        conn=DBUtil.ConnectToDataBase()
        print DBUtil.UpdateRecordInTable(conn, 'test_run_env', "where run_id = '%s'" % TestRunID[0], status='In-Progress')
        conn.close()
        currentTestSetStatus = 'In-Progress'
        #Insert an entry to the TestResultsEnv table
        sTimeStamp = TimeStamp() #used for run_id
        #sTestResultsRunId = TestRunID[0] + '-' + sTimeStamp
        sTestResultsRunId = TestRunID[0]# + sTimeStamp
        #test set start time
        conn=DBUtil.ConnectToDataBase()
        now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
        conn.close()
        sTestSetStartTime = str(now[0][0])
        iTestSetStartTime = now[0][0]
        #cur.execute("insert into test_env_results (run_id,rundescription,tester_id,status,teststarttime) values ('%s','%s','%s','In-Progress','%s')" % (sTestResultsRunId, TestRunID[1], Userid, sTestSetStartTime))
        #conn.commit()
        conn=DBUtil.ConnectToDataBase()
        DBUtil.UpdateRecordInTable(conn, 'test_env_results', "Where run_id = '%s' and tester_id = '%s'" % (sTestResultsRunId, Userid), status='In-Progress', teststarttime='%s' % (sTestSetStartTime))
        conn.close()

        # Find the type of dataset we want to run for given testset
        #no data Type is used in our framework thats why it is ommitted.
        #DataTypeList = DBUtil.GetData(conn, "Select data_type From test_run_env Where run_id = '%s'" % TestRunID[0], False)
        #DataType = DataTypeList[0][0]
        DataType=""

        #Find Test Cases in this Test Set & add it to test_run table
        #TestCaseLists = DBUtil.GetData(conn, "Select TC_ID From Test_Sets Where testset_id = '%s' order by id" % TestRunID[1], False) #and data_type
        #for TestCaseID in TestCaseLists:
            #Insert each test case id to the test_run table
         #   DBUtil.InsertNewRecordInToTable(conn, 'test_run', run_id=sTestResultsRunId, tc_id=list(TestCaseID)[0])

        #This step will remain here for now, just to make sure test case is added in the previous one
        #Find all test cases added in the test_run table for the current run id
        conn=DBUtil.ConnectToDataBase()
        TestCaseLists = DBUtil.GetData(conn, "Select TC_ID From test_run Where run_id = '%s'" % TestRunID[0], False)
        conn.close()
        #HYBRID RUN IMPLEMENTED HERE
        AutomationList=[]
        run_type=""
        for each in TestCaseLists:
            print each
            test_case_id=each[0]
            #check if its forced or not
            """if Rerun==False:
                query="select property from test_case_tag where tc_id='%s' and name='Status'"%test_case_id
            else:
                query="select property from result_test_case_tag where tc_id='%s' and name='Status' and run_id='%s'"%(test_case_id,referred_run_id)
            """
            query="select name from result_test_case_tag where tc_id='%s' and property='Status' and run_id='%s'"%(test_case_id,TestRunID[0])
            conn=DBUtil.ConnectToDataBase()
            forced=DBUtil.GetData(conn,query)
            conn.close()
            if forced[0]=='Forced':
                continue
            else:
                temp=[]
                temp.append(test_case_id)
                temp=tuple(temp)
                AutomationList.append(temp)
        AutomationListWithType=[]
        for each in AutomationList:
            """if Rerun==False:
                query="select tsl.steptype from test_cases tc,test_steps_list tsl,test_steps ts where tc.tc_id=ts.tc_id and tsl.step_id=ts.step_id and tc.tc_id='%s' order by ts.teststepsequence"%each[0]
            else:
                query="select tsl.steptype from result_test_cases tc,result_test_steps_list tsl,result_test_steps ts where tsl.run_id=ts.run_id and tc.tc_id=ts.tc_id and tc.run_id=ts.run_id and tsl.step_id=ts.step_id and tc.tc_id='%s' and tc.run_id='%s' order by ts.teststepsequence"%(each[0],referred_run_id)
            """
            query="select tsl.steptype from result_test_cases tc,result_test_steps_list tsl,result_test_steps ts where tsl.run_id=ts.run_id and tc.tc_id=ts.tc_id and tc.run_id=ts.run_id and tsl.step_id=ts.step_id and tc.tc_id='%s' and tc.run_id='%s' order by ts.teststepsequence"%(each[0],TestRunID[0])
            conn=DBUtil.ConnectToDataBase()
            status_list=DBUtil.GetData(conn,query)
            conn.close()
            for eachstatus in status_list:
                if eachstatus=='manual':
                    test_case_type='manual'
                    break
                else:
                    test_case_type='automation'
            temp=[]
            temp.append(each[0])
            temp.append(test_case_type)
            temp=tuple(temp)
            AutomationListWithType.append(temp)
        Automation=[]
        automation_count=0
        manual_count=0
        for each in AutomationListWithType:
            if each[1]=='automation':
                automation_count+=1
                temp=[]
                temp.append(each[0])
                temp=tuple(temp)
                Automation.append(temp)
            else:
                manual_count+=1
                continue
        if len(TestCaseLists)>0:
            forced_count=len(TestCaseLists)-(automation_count+manual_count)
            if automation_count>0 and automation_count==len(TestCaseLists)and (forced_count==0 and manual_count==0):
                run_type="Automation"
            elif (forced_count>0 or manual_count>0) and automation_count>0:
                run_type="Hybrid"
            else:
                run_type="Manual"
        Dict={}
        Dict.update({'run_type':run_type})
        sWhereQuery="where run_id='%s'" %TestRunID[0]
        conn=DBUtil.ConnectToDataBase()
        print DBUtil.UpdateRecordInTable(conn,"test_run_env",sWhereQuery,**Dict)
        conn.close()
        TestCaseLists=[]
        TestCaseLists=Automation
        if len(TestCaseLists) > 0:
            print "Running Test cases from list : ", TestCaseLists[0:len(TestCaseLists)]
            CommonUtil.ExecLog(sModuleInfo, "Running Test cases from list : %s" % TestCaseLists[0:len(TestCaseLists)], 1)
            print "Total number of test cases ", len(TestCaseLists)
        else:
            print "No test cases found for the current user :", Userid
            CommonUtil.ExecLog(sModuleInfo, "No test cases found for the current user : %s" % Userid, 2)
            return False
        #TestCaseLists = list(TestCaseLists[0])
        for TestCaseID in TestCaseLists:
            Global.sTestStepExecLogId = "MainDriver"
            StepSeq = 1
            TCID = list(TestCaseID)[0]
            print "-------------*************--------------"
            """if Rerun==False:
                TestCaseName = DBUtil.GetData(conn, "Select tc_name From test_cases Where tc_id = '%s'" % TCID, False)
            else:
                TestCaseName = DBUtil.GetData(conn, "Select tc_name From result_test_cases Where tc_id = '%s' and run_id='%s'" % (TCID,referred_run_id), False)
            """
            conn=DBUtil.ConnectToDataBase()
            TestCaseName = DBUtil.GetData(conn, "Select tc_name From result_test_cases Where tc_id = '%s' and run_id='%s'" % (TCID,TestRunID[0]), False)
            conn.close()
            #Create Log Folder for the TC
            #get the config_global.ini
            config=ConfigParser.ConfigParser()
            global_config_file=os.getcwd()+os.sep+'global_config.ini'
            config.read(global_config_file)
            try:
                log_file_path=config.get('sectionOne', 'temp_run_file_path')
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()        
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                print Error_Detail
            Global.TCLogFolder=log_file_path+os.sep+(TestRunID[0].replace(':','-')+os.sep+TCID.replace(":",'-'))
            #Global.TCLogFolder = (Global.NetworkLogFolder + os.sep + sTestResultsRunId + os.sep + TCID + "_" + CommonUtil.TimeStamp("utcstring")).replace(":", "-")
            test_case_folder=log_file_path+os.sep+(TestRunID[0].replace(':','-')+os.sep+TCID.replace(":",'-'))
            update_global_config('sectionOne', 'test_case',TCID)
            update_global_config('sectionOne','test_case_folder',test_case_folder)
            log_folder=test_case_folder+os.sep+'Log'
            update_global_config('sectionOne', 'log_folder',log_folder)
            screenshot_folder=test_case_folder+os.sep+'screenshots'
            update_global_config('sectionOne', 'screen_capture_folder',screenshot_folder)
            
            config=ConfigParser.ConfigParser()
            config.read(global_config_file)
            
            #create_test_case_folder
            test_case_folder=config.get('sectionOne','test_case_folder')
            FL.CreateFolder(test_case_folder)
            
            #FL.CreateFolder(Global.TCLogFolder + os.sep + "ProductLog")
            log_folder=config.get('sectionOne','log_folder')
            FL.CreateFolder(log_folder)
            
            #FL.CreateFolder(Global.TCLogFolder + os.sep + "Screenshots")
            #creating ScreenShot File
            screen_capture_folder=config.get('sectionOne','screen_capture_folder')
            FL.CreateFolder(screen_capture_folder)
            
            print "Running Test case id : %s :: %s" % (TCID, TestCaseName[0])
            CommonUtil.ExecLog(sModuleInfo, "-------------*************--------------", 1)
            CommonUtil.ExecLog(sModuleInfo, "Running Test case id : %s :: %s" % (TCID, TestCaseName), 1)


            #test Case start time
            conn=DBUtil.ConnectToDataBase()
            now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
            conn.close()
            
            sTestCaseStartTime = str(now[0][0])
            iTestCaseStartTime = now[0][0]

            #cur.execute("insert into test_case_results (run_id,tc_id,status,teststarttime ) values ('%s','%s','In-Progress','%s')" % (sTestResultsRunId, TCID, sTestCaseStartTime))
            #conn.commit()
            condition="where run_id='"+sTestResultsRunId+"' and tc_id='"+TCID+"'"
            conn=DBUtil.ConnectToDataBase()
            print DBUtil.UpdateRecordInTable(conn,"test_case_results", condition,status='In-Progress',teststarttime=sTestCaseStartTime)
            conn.close()
            #Get Test Case Index to be inserted to test_step_results table
            conn=DBUtil.ConnectToDataBase()
            TestCaseResultIndex = DBUtil.GetData(conn, "Select id From test_case_results where run_id = '%s' and TC_ID = '%s' Order By id desc limit 1" % (sTestResultsRunId, TCID), False)
            conn.close()
            #get the test case steps for this test case
            #TestStepsList = DBUtil.GetData(conn,"Select teststepname From TestSteps where TC_ID = '%s' Order By teststepsequence" %TCID,False)
            """if Rerun==False:
                TestStepsList = DBUtil.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,ts.test_step_type From Test_Steps ts,test_steps_list tsl where TC_ID = '%s' and ts.step_id = tsl.step_id and tsl.stepenable='true' Order By teststepsequence" % TCID, False)
            else:
                TestStepsList = DBUtil.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,ts.test_step_type From result_test_steps ts,result_test_steps_list tsl where ts.run_id=tsl.run_id and TC_ID = '%s' and ts.step_id = tsl.step_id and tsl.stepenable='true' and ts.run_id='%s' Order By teststepsequence" % (TCID,referred_run_id), False)
            """
            conn=DBUtil.ConnectToDataBase()
            TestStepsList = DBUtil.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.driver,tsl.steptype,tsl.data_required,tsl.step_editable From result_test_steps ts,result_test_steps_list tsl where ts.run_id=tsl.run_id and TC_ID = '%s' and ts.step_id = tsl.step_id and tsl.stepenable='true' and ts.run_id='%s' Order By teststepsequence" % (TCID,TestRunID[0]), False)
            conn.close()
            Stepscount = len(TestStepsList)
            sTestStepResultList = []
            #get the client name for this test case
            #sClientName = TestRunID[4]
            #sClientName=(TestRunID[4].split("("))[0].strip()
            #print sClientName
            """if Rerun==False:
                #DataSetList = DBUtil.GetData(conn, "Select tcdatasetid from test_case_datasets where tc_id='%s' and data_type='%s'" % (TCID, DataType), False) # Later we can add dataset tag like multilang here.
                DataSetList = DBUtil.GetData(conn, "Select tcdatasetid from test_case_datasets where tc_id='%s'" % (TCID), False)
            else:
                DataSetList = DBUtil.GetData(conn, "Select tcdatasetid from result_test_case_datasets where tc_id='%s' and run_id='%s'" % (TCID,referred_run_id), False)
            """
            conn=DBUtil.ConnectToDataBase()
            DataSetList = DBUtil.GetData(conn, "Select tcdatasetid from result_test_case_datasets where tc_id='%s' and run_id='%s'" % (TCID,TestRunID[0]), False)
            conn.close()
            if len(DataSetList) == 0:
                #This condition is for test cases which dont have any input data
                DataSetList.append('NoDataSetFound')
            for EachDataSet in DataSetList:
                #Check if this is a performance test case
                """if DataType == 'Performance':
                    #this is a performance test case
                    PerfQ = Queue.Queue()
                    PerfThread = threading.Thread(target=Performance.CollectProcessMemory, args=(TestStepsList[StepSeq - 1][1], PerfQ))
                    PerfThread.start()
                    PerfQ.put('Start')
                """
                while StepSeq <= Stepscount:
                    # Beginning of a Test Step
                    print "Step: ", TestStepsList[StepSeq - 1][1]
                    CommonUtil.ExecLog(sModuleInfo, "Step : %s" % TestStepsList[StepSeq - 1][1], 1)
                    testcasecontinue=False
                    Conn=DBUtil.ConnectToDataBase()
                    query="select description from master_data where field='continue' and value='point' and id ='%s'"%(TCID+'_s'+str(StepSeq))
                    test_case_continue=DBUtil.GetData(Conn,query,False)
                    Conn.close()
                    if test_case_continue[0][0]=='yes':
                        testcasecontinue=True
                    else:
                        testcasecontinue=False
                    #if DataType == 'Performance':
                    #    PerfQ.put(TestStepsList[StepSeq - 1][1])
                    #Check if the current test step is a Performance Test Step
                    if TestStepsList[StepSeq - 1][4] == 'Performance':
                        Global.sTestStepType = TestStepsList[StepSeq - 1][4]

                    #Test Step Log id
                    Global.sTestStepExecLogId = sTestResultsRunId + TCID + str(TestStepsList[StepSeq - 1][0]) + str(StepSeq)
                    
                    #open a file handler and write it to it
                    update_global_config('sectionOne', 'sTestStepExecLogId', Global.sTestStepExecLogId)
                    # Test Step start time
                    conn=DBUtil.ConnectToDataBase()
                    now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
                    conn.close()
                    sTestStepStartTime = str(now[0][0])
                    #TestStepStartTime = now[0][0]
                    TestStepStartTime = time.clock()
                    # Memory calculation at the beginning of test step
                    WinMemBegin = CommonUtil.PhysicalAvailableMemory()#MemoryManager.winmem() 
                    #update test_step_results table
                    #cur.execute("insert into test_step_results (run_id,tc_id,teststep_id,teststepsequence,status,stepstarttime,logid,start_memory,testcaseresulttindex ) values ('%s','%s','%d','%d','In-Progress','%s','%s', '%s', '%d')" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], sTestStepStartTime, Global.sTestStepExecLogId, WinMemBegin, TestCaseResultIndex[0][0]))
                    #conn.commit()
                    condition="where run_id='"+sTestResultsRunId+"' and tc_id='"+TCID+"' and teststep_id='"+str(TestStepsList[StepSeq - 1][0])+"' and teststepsequence='"+str(TestStepsList[StepSeq - 1][2])+"'"
                    Dict={'teststepsequence':TestStepsList[StepSeq - 1][2],'status':'In-Progress','stepstarttime':sTestStepStartTime,'logid':Global.sTestStepExecLogId,'start_memory':WinMemBegin,'testcaseresulttindex':TestCaseResultIndex[0][0]}
                    conn=DBUtil.ConnectToDataBase()
                    DBUtil.UpdateRecordInTable(conn,"test_step_results",condition,**Dict)
                    conn.close()
                    steps_data=[]
                    #get the steps data from here
                    if TestStepsList[StepSeq-1][5] and TestStepsList[StepSeq-1][6]:
                        #for the edit data steps
                        container_id_data_query="select ctd.curname,ctd.newname from test_steps_data tsd, container_type_data ctd where tsd.testdatasetid = ctd.dataid and tcdatasetid = 'CLI-0382ds' and teststepseq = 13060 and ctd.curname Ilike '%_s2%'"
                    elif TestStepsList[StepSeq-1][5] and not TestStepsList[StepSeq-1][6]:
                        container_id_data_query="select ctd.curname,ctd.newname from test_steps_data tsd, container_type_data ctd where tsd.testdatasetid = ctd.dataid and tcdatasetid = '%s' and teststepseq = %d and ctd.curname Ilike '%%_s%s%%'"%(EachDataSet[0],int(TestStepsList[StepSeq-1][2]),StepSeq)
                        conn=DBUtil.ConnectToDataBase()
                        container_data_details=DBUtil.GetData(conn,container_id_data_query,False)
                        conn.close()
                        steps_data=[]
                        for each_data_id in container_data_details:
                            From_Data = DataFetching.Get_PIM_Data_By_Id(each_data_id[0])
                            steps_data.append(From_Data)
                    else:
                        steps_data=[]
                    print "steps data for #%d: "%StepSeq,steps_data
                    CommonUtil.ExecLog(sModuleInfo,"steps data for #%d: %s"%(StepSeq,str(steps_data)),1)
                    try:
                        #while True:
                            #If threading is enabled
                            #if Global.ThreadingEnabled:
                            q = Queue.Queue()
                            #Call Test Step
                            #if TestStepsList[StepSeq - 1][3] == "Futureshop":
                            if TestStepsList[StepSeq-1][3] in Driver_list:    
                                #If threading is enabled
                                #import pdb
                                #pdb.set_trace()
                                module_name=importlib.import_module(TestStepsList[StepSeq-1][3])
                                if Global.ThreadingEnabled:
                                    stepThread = threading.Thread(target=module_name.ExecuteTestSteps, args=(conn, TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q,TestRunID[0]))
                                else:
                                    #from Drivers import Futureshop
                                    step_name=TestStepsList[StepSeq-1][1]
                                    step_name=step_name.lower().replace(' ','_')
                                    functionTocall=getattr(module_name, step_name)
                                    sStepResult = functionTocall(dependency_list_final,steps_data)
                                    if sStepResult in passed_tag_list:
                                        sStepResult='PASSED'
                                    if sStepResult in failed_tag_list:
                                        sStepResult='FAILED'
                                    q.put(sStepResult)
                                    #sStepResult = module_name.ExecuteTestSteps(TestRunID[0],TestStepsList[StepSeq - 1][1],q,dependency_list,steps_data)
                                    #sStepResult = Futureshop.ExecuteTestSteps(TestStepsList[StepSeq - 1][1],q,dependency_list,steps_data)

                            else:
                                #If threading is enabled
                                if Global.ThreadingEnabled:
                                    stepThread = threading.Thread(target=ExecuteTestSteps, args=(TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q))
                                else:
                                    sStepResult = ExecuteTestSteps(TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q)

                            #If threading is enabled
                            if Global.ThreadingEnabled:
                                #Start the thread
                                print "Starting Test Step Thread.."
                                stepThread.start()
                                #Wait for the Thread to finish or until timeout
                                print "Waiting for Test Step Thread to finish..for (seconds) :", Global.DefaultTestStepTimeout
                                stepThread.join(Global.DefaultTestStepTimeout)
                                #Get the return value from the ExecuteTestStep fn via Queue
                                try:
                                    sStepResult = q.get(True, 5)
                                    print "Test Step Thread Ended.."
                                except Queue.Empty:
                                    print "Test Step did not return after default timeout (secs) : ", Global.DefaultTestStepTimeout
                                    sStepResult = "Failed"

                                    #Clean up
                                    if stepThread.isAlive():
                                        print "thread still alive"
                                        #stepThread.__stop()
                                        try:
                                            stepThread._Thread__stop()
                                            while stepThread.isAlive():
                                                time.sleep(1)
                                                print "Thread is still alive"
                                        except:
                                            print "Thread could not be terminated"

                    except Exception, e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()        
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                        print Error_Detail
                        CommonUtil.ExecLog(sModuleInfo, "Exception occurred in test step : %s" % Error_Detail, 3)
                        sStepResult = "Failed"

                    #Check if the db connection is alive or timed out
                    #if DBUtil.IsDBConnectionGood(conn) == False:
                    #    print "DB connection is bad"
                    #    CommonUtil.ExecLog(sModuleInfo, "DB connection error", 3)
                    try:
                        conn.close()
                    except Exception, e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()        
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                        print Error_Detail
                        CommonUtil.ExecLog(sModuleInfo, "Exception closing DB connection:%s" % Error_Detail, 2)
                    #test Step End time
                    conn=DBUtil.ConnectToDataBase()
                    now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
                    conn.close()
                    sTestStepEndTime = str(now[0][0])
                    #TestStepEndTime = now[0][0]
                    TestStepEndTime = time.clock()

                    # Time it took to run the test step
                    TimeDiff = TestStepEndTime - TestStepStartTime
                    #TimeInSec = TimeDiff.seconds
                    TimeInSec = int(TimeDiff)
                    TestStepDuration = CommonUtil.FormatSeconds(TimeInSec)

                    # Memory at the end of Test Step
                    WinMemEnd = CommonUtil.PhysicalAvailableMemory() #MemoryManager.winmem()

                    # Total memory consumed during the test step
                    TestStepMemConsumed = WinMemBegin - WinMemEnd



                    #add result of each step to a list; for a test case to pass all steps should be pass; atleast one Failed makes it 'Fail' else 'Warning' or 'Blocked'
                    if sStepResult:
                        sTestStepResultList.append(sStepResult.upper())
                    else:
                        sTestStepResultList.append("FAILED")
                        print "sStepResult : ", sStepResult
                        CommonUtil.ExecLog(sModuleInfo, "sStepResult : %s" % sStepResult, 1)
                        sStepResult = "Failed"

                    #Take ScreenShot
                    CommonUtil.TakeScreenShot(sStepResult + "_" + TestStepsList[StepSeq - 1][1])

                    #Update Results
                    if sStepResult.upper() == "PASSED":
                        #Step Passed
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Passed"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Passed" % TestStepsList[StepSeq - 1][1], 1)
                        #Update Test Step Results table
                        conn=DBUtil.ConnectToDataBase()
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Passed',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        conn.close()
                    elif sStepResult.upper() == "WARNING":
                        #Step has Warning, but continue running next test step for this test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Warning"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Warning" % TestStepsList[StepSeq - 1][1], 2)
                        #Update Test Step Results table
                        conn=DBUtil.ConnectToDataBase()
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Warning',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        conn.close()
                        if not testcasecontinue:
                            break
                    elif sStepResult.upper() == "NOT RUN":
                        #Step has Warning, but continue running next test step for this test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Not Run"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Not Run" % TestStepsList[StepSeq - 1][1], 2)
                        #Update Test Step Results table
                        conn=DBUtil.ConnectToDataBase()
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Not Run',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        conn.close()
                    elif sStepResult.upper() == "FAILED":
                        #Step has a Critial failure, fail the test step and test case. go to next test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Failed Failure"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Failed Failure" % TestStepsList[StepSeq - 1][1], 3)
                        #Update Test Step Results table
                        conn=DBUtil.ConnectToDataBase()
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Failed',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        conn.close()
                        #Discontinue this test case
                        #break
                        #for continuing the test cases if failed
                        if not testcasecontinue:
                            break
                    elif sStepResult.upper() == "BLOCKED":
                        #Step is Blocked, Block the test step and test case. go to next test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Blocked"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Blocked" % TestStepsList[StepSeq - 1][1], 3)
                        #Update Test Step Results table
                        conn=DBUtil.ConnectToDataBase()
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Blocked',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        conn.close()
                        #Discontinue this test case
                        #break
                        #for continuing the test cases if failed
                        
                    #End Test Step
                    #increment step counter
                    StepSeq = StepSeq + 1

                    #Check if Test Set status is 'Cancelled' When it is stopped from Website
                    conn=DBUtil.ConnectToDataBase()
                    currentTestSetStatus = DBUtil.GetData(conn, "Select status"
                              " From test_run_env"
                              " Where run_id = '%s'" % sTestResultsRunId, False)
                    conn.close()
                    currentTestSetStatus = currentTestSetStatus[0][0]
                    if currentTestSetStatus == 'Cancelled':
                        print "Test Run status is Cancelled. Exiting the current Test Case... ", TCID
                        CommonUtil.ExecLog(sModuleInfo, "Test Run status is Cancelled. Exiting the current Test Case...%s" % TCID, 2)
                        break
                if DataType == 'Performance':
                    PerfQ.put('Stop')
            #else:
            #    print "Unknown client name : ", sClientName

            #End of test case
            #test Case End time
            conn=DBUtil.ConnectToDataBase()
            now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
            conn.close()
            sTestCaseEndTime = str(now[0][0])
            iTestCaseEndTime = now[0][0]

            #Decide if Test Case Pass/Failed
            if 'BLOCKED' in sTestStepResultList:
                print "Test Case Blocked"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Blocked", 3)
                sTestCaseStatus = "Blocked"
            elif 'FAILED' in sTestStepResultList:
                print "Test Case Failed"
                step_index=1
                for each in sTestStepResultList:
                    if each=='FAILED':
                        break
                    else:
                        step_index+=1
                datasetid=TestCaseID[0]+'_s'+str(step_index)
                query="select description from master_data where field='verification' and value='point' and id='%s'"%datasetid
                #Conn=GetConnection()
                conn=DBUtil.ConnectToDataBase()
                status=DBUtil.GetData(conn,query,False)
                conn.close()
                if status[0][0]=="yes":
                    sTestCaseStatus='Failed'
                else:
                    sTestCaseStatus='Blocked'
                CommonUtil.ExecLog(sModuleInfo, "Test Case "+sTestCaseStatus, 3)
            elif 'WARNING' in sTestStepResultList:
                print "Test Case Contain Warning(s)"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Contain Warning(s)", 2)
                sTestCaseStatus = "Failed"
            elif 'NOT RUN' in sTestStepResultList:
                print "Test Case Contain Not Run Steps"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Contain Warning(s)", 2)
                sTestCaseStatus = "Failed"
            elif 'PASSED' in sTestStepResultList:
                print "Test Case Passed"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Passed", 1)
                sTestCaseStatus = "Passed"
            else:
                print "Test Case Status Unknown"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Status Unknown", 2)
                sTestCaseStatus = "Unknown"

            # Time it took to run the test case
            TimeDiff = iTestCaseEndTime - iTestCaseStartTime
            TimeInSec = TimeDiff.seconds
            TestCaseDuration = CommonUtil.FormatSeconds(TimeInSec)

            #Collect Log if Test case Failed
            #if sTestCaseStatus != "Passed":
            #Get DTS Logs
            print CommonUtil.GetProductLog()

            #Zip the folder
            config=ConfigParser.ConfigParser()
            config.read(global_config_file)
            #removing duplicates line from here. 
            current_log_file=config.get('sectionOne','log_folder')+os.sep+'temp.log'
            temp_log_file=config.get('sectionOne','log_folder')+os.sep+TCID+'.log'
            lines_seen=set()
            outfile=open(temp_log_file,'w')
            for line in open(current_log_file,'r'):
                if line not in lines_seen:
                    outfile.write(line)
                    lines_seen.add(line)
            outfile.close()
            FL.DeleteFile(current_log_file)
            FL.RenameFile(config.get('sectionOne','log_folder'), 'temp.log',TCID+'.log')
            TCLogFile = CommonUtil.ZipFolder(config.get('sectionOne','test_case_folder'),config.get('sectionOne','test_case_folder') + ".zip")
            #Delete the folder
            FL.DeleteFolder(config.get('sectionOne','test_case_folder'))
            #upload will go here.
            upload_link='http://localhost:8000/Home/UploadZip'
            register_openers()
            datagen, headers = multipart_encode({
                'categoryID' : 1,
                'cID'        : -3,
                'FileType'   : 'zip',
                'name'       : sTestResultsRunId,
                'file1'      : open(config.get('sectionOne','test_case_folder') + ".zip")
            })
            request = urllib2.Request(upload_link, datagen, headers)
            #Find Test case failed reason
            try:
                FailReason = CommonUtil.FindTestCaseFailedReason(conn, sTestResultsRunId, TCID)
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()        
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                print Error_Detail
                print "Unable to find Fail Reason for Test case: ", TCID
                FailReason = ""

            #Update test case result
            conn=DBUtil.ConnectToDataBase()
            DBUtil.UpdateRecordInTable(conn, 'test_case_results', "Where run_id = '%s' and tc_id = '%s'" % (sTestResultsRunId, TCID), status='%s' % (sTestCaseStatus), testendtime='%s' % (sTestCaseEndTime), duration='%s' % (TestCaseDuration), failreason='%s' % (FailReason), logid='%s' % (TCLogFile))
            conn.close()
            #Update Performance Results if Its a Performance test case And if test case had Passed
            if DataType == 'Performance' and sTestCaseStatus == 'Passed':
                product_version = CommonUtil.GetProductVersion()
                print "machine_os:", TestRunID[4]
                print "tc_id:", list(TestCaseID)[0]
                print "tc_name:", TestCaseName[0]
                print "tc_section:", list(TestCaseID)[0]
                print "run_id:", sTestResultsRunId
                print "duration:", Global.transaction_duration
                print "memory_avg:", Global.transaction_deltamemory
                print "memory_peak:", Global.transaction_deltamemory
                HWobj = Performance.ComputerHWInfo()
                hwmodel = HWobj.CompInfo().HWModel
                print "HW Model:", hwmodel

                conn=DBUtil.ConnectToDataBase()
                DBUtil.InsertNewRecordInToTable(conn, 'performance_results',
                        product_version=product_version,
                        tc_id=list(TestCaseID)[0],
                        run_id=sTestResultsRunId,
                        machine_os=TestRunID[4],
                        duration=Global.transaction_duration,
                        memory_avg=Global.transaction_startmemory,
                        memory_peak=Global.transaction_endmemory,
                        hw_model=hwmodel)
                conn.close()
            #Check if Test Set status is 'Cancelled' When it is stopped from Website
            conn=DBUtil.ConnectToDataBase()
            currentTestSetStatus = DBUtil.GetData(conn, "Select status"
                      " From test_run_env"
                      " Where run_id = '%s'" % sTestResultsRunId, False)
            conn.close()
            currentTestSetStatus = currentTestSetStatus[0][0]

            if currentTestSetStatus == 'Cancelled':
                print "Test Run status is Cancelled. Exiting the current Test Set... ", sTestResultsRunId
                CommonUtil.ExecLog(sModuleInfo, "Test Run status is Cancelled. Exiting the current Test Set...%s" % sTestResultsRunId, 2)
                break


        #End of Test Set    
        #Update entry in the TestResultsEnv table that this run is completed
        #test set end time
        conn=DBUtil.ConnectToDataBase()
        now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
        conn.close()
        sTestSetEndTime = str(now[0][0])
        iTestSetEndTime = now[0][0]
        TestSetDuration = CommonUtil.FormatSeconds((iTestSetEndTime - iTestSetStartTime).seconds)

        #Update Test Run tables based on the Test Set Status
        if currentTestSetStatus == 'Cancelled':
            conn=DBUtil.ConnectToDataBase()
            DBUtil.UpdateRecordInTable(conn, 'test_env_results', "Where run_id = '%s' and tester_id = '%s'" % (sTestResultsRunId, Userid), status='Cancelled', testendtime='%s' % (sTestSetEndTime), duration='%s' % (TestSetDuration))
            conn.close()
            print "Test Set Cancelled by the User"
            CommonUtil.ExecLog(sModuleInfo, "Test Set Cancelled by the User", 1)
        else:
            if automation_count>0 and automation_count==len(TestCaseLists)and (forced_count==0 and manual_count==0):
                conn=DBUtil.ConnectToDataBase()
                print DBUtil.UpdateRecordInTable(conn, 'test_env_results', "Where run_id = '%s' and tester_id = '%s'" % (sTestResultsRunId, Userid), status='Complete', testendtime='%s' % (sTestSetEndTime), duration='%s' % (TestSetDuration))
                conn.close()
                #Update test_run_env schedule table with status so that this Test Set will not be run again
                conn=DBUtil.ConnectToDataBase()
                print DBUtil.UpdateRecordInTable(conn, 'test_run_env', "Where run_id = '%s' and tester_id = '%s'" % (TestRunID[0], Userid), status='Complete')
                conn.close()
                print "Test Set Completed"
            #CommonUtil.ExecLog(sModuleInfo, "Test Set Completed", 1)

            Global.sTestStepExecLogId = "MainDriver"

            try:
                #Send Summary Email
                oConn=DBUtil.ConnectToDataBase()
                ToEmailAddress = DBUtil.GetData(oConn, "select email_notification from test_run_env where run_id = '%s'" % (TestRunID[0]))
                TestObjective = DBUtil.GetData(oConn, "select test_objective from test_run_env where run_id = '"+TestRunID[0]+"'")
                tester = DBUtil.GetData(oConn, "select assigned_tester from test_run_env where run_id = '"+TestRunID[0]+"'")
                #import EmailNotify
                #EmailNotify.Complete_Email(allEmailIds,run_id,TestObjective,status,'','')
                 
                global list
                pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % TestRunID[0]
                passed = DBUtil.GetData(oConn, pass_query)
                list.append(passed[0])
                fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % TestRunID[0]
                fail = DBUtil.GetData(oConn, fail_query)
                list.append(fail[0])
                blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % TestRunID[0]
                blocked = DBUtil.GetData(oConn, blocked_query)
                list.append(blocked[0])
                progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % TestRunID[0]
                progress = DBUtil.GetData(oConn, progress_query)
                list.append(progress[0])
                submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % TestRunID[0]
                submitted = DBUtil.GetData(oConn, submitted_query)
                list.append(submitted[0])
                skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % TestRunID[0]
                skipped = DBUtil.GetData(oConn, skipped_query)
                list.append(skipped[0])
                total_query = "select count(*) from test_case_results where run_id='%s'" % TestRunID[0]
                total = DBUtil.GetData(oConn, total_query)
                list.append(total[0])
                duration = DBUtil.GetData(
                    oConn,
                    "select to_char(now()-teststarttime,'HH24:MI:SS') as Duration from test_env_results where run_id = '" +
                    TestRunID[0] +
                    "'")
                
                oConn.close()
                if ToEmailAddress[0]:
                    #conn=DBUtil.ConnectToDataBase()
                    #email notify
                    try:
                        urllib2.urlopen("http://www.google.com").close()
                        EmailNotify.Complete_Email(ToEmailAddress[0],TestRunID[0],TestObjective[0],status,list,tester,duration,'','')
                        print "connected"
                        results = ['OK']
                    except urllib2.URLError:
                        print "disconnected"
                        results = ['NOK']
                    """try:
                        Summary = DBUtil.GetData(conn, "select * from test_env_results where run_id = '%s'" % (TestRunID[0]), False)
                        CommonUtil.SendEmail(ToEmailAddress[0][0], TestRunID[0], Summary)
                    except Exception, e:
                        conn.close()
                        return "pass" """
                

            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()        
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_Detail = ((str(exc_type).replace("type ", "Error Type: ")) + ";" +  "Error Message: " + str(exc_obj) +";" + "File Name: " + fname + ";" + "Line: "+ str(exc_tb.tb_lineno))
                print Error_Detail
                return "pass"
        #Copy the Automation Log to Network Folder
        #if FL.CopyFile(CommonUtil.hdlr.baseFilename, Global.NetworkLogFolder + os.sep + TestRunID[0].replace(':', '-')) == True:
        #    CommonUtil.ClearLog()

    #Close DB Connection
    conn.close()
    return "pass"

if __name__ == "__main__":

    Global.sTestStepExecLogId = "MainDriver"
    print main()



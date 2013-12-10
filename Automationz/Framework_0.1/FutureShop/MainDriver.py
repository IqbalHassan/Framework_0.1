# -*- coding: cp1252 -*-
import os, sys
import time, datetime
import threading, Queue
import inspect
import DataBaseUtilities as DBUtil
import FileUtilities as FL
import Global, CommonUtil
import Sub_Driver_Futureshop
#import FSDriver
import Performance

if os.name == 'nt':
    location = "X:\\Actions\\Common Tasks\\PythonScripts\\"
    if location not in sys.path:
        sys.path.append(location)

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
            return CommonUtil.LogCriticalException(sModuleInfo, e)

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

    try:
        conn = DBUtil.ConnectToDataBase()
    except Exception, e:
        CommonUtil.ExecLog(sModuleInfo, "Exception : %s" % e , 3)
        #print "unable to connect to the database"
    CommonUtil.ExecLog(sModuleInfo, "Database connection successful" , 1)
    cur = conn.cursor()
    Userid = (CommonUtil.GetLocalUser()).lower()
    UserList = DBUtil.GetData(conn, "Select User_Names from permitted_user_list")
    if Userid not in UserList:
        CommonUtil.ExecLog(sModuleInfo, "User don't have permission to run the tests" , 3)
        return "You Don't Have Permission"

    #Find Test Runs scheduled for this user from test_run_env table
    TestRunLists = DBUtil.GetData(conn, "Select run_id"
                                  ",rundescription"
                                  ",tester_id"
                                  ",machine_os"
                                  ",client"
                                  ",data_type"
                                  ",test_run_type"
                                  " From test_run_env"
                                  " Where tester_id = '%s' and (status = 'Submitted')" % Userid, False)
    if len(TestRunLists) > 0:
        print "Running Test cases from Test Set : ", TestRunLists[0:len(TestRunLists)]
        CommonUtil.ExecLog(sModuleInfo, "Running Test cases from Test Set : %s" % TestRunLists[0:len(TestRunLists)], 1)
    else:
        print "No Test Run Schedule found for the current user :", Userid
        CommonUtil.ExecLog(sModuleInfo, "No Test Run Schedule found for the current user : %s" % Userid, 2)
        return False

    #Loop thru all the test runs scheduled for this user
    for TestRunID in TestRunLists:
        #TestResultsEnv Table
        #Update test_run_env table with status for the current TestRunId
        print DBUtil.UpdateRecordInTable(conn, 'test_run_env', "where run_id = '%s'" % TestRunID[0], status='In-Progress')
        currentTestSetStatus = 'In-Progress'
        #Insert an entry to the TestResultsEnv table
        sTimeStamp = TimeStamp() #used for run_id
        #sTestResultsRunId = TestRunID[0] + '-' + sTimeStamp
        sTestResultsRunId = TestRunID[0]# + sTimeStamp
        #test set start time
        now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
        sTestSetStartTime = str(now[0][0])
        iTestSetStartTime = now[0][0]
        cur.execute("insert into test_env_results (run_id,rundescription,tester_id,status,teststarttime) values ('%s','%s','%s','In-Progress','%s')" % (sTestResultsRunId, TestRunID[1], Userid, sTestSetStartTime))
        conn.commit()

        # Find the type of dataset we want to run for given testset
        DataTypeList = DBUtil.GetData(conn, "Select data_type From test_run_env Where run_id = '%s'" % TestRunID[0], False)
        DataType = DataTypeList[0][0]

        #Find Test Cases in this Test Set & add it to test_run table
        TestCaseLists = DBUtil.GetData(conn, "Select TC_ID From Test_Sets Where testset_id = '%s' order by id" % TestRunID[1], False) #and data_type
        for TestCaseID in TestCaseLists:
            #Insert each test case id to the test_run table
            DBUtil.InsertNewRecordInToTable(conn, 'test_run', run_id=sTestResultsRunId, tc_id=list(TestCaseID)[0])

        #This step will remain here for now, just to make sure test case is added in the previous one
        #Find all test cases added in the test_run table for the current run id
        TestCaseLists = DBUtil.GetData(conn, "Select TC_ID From test_run Where run_id = '%s'" % TestRunID[0], False)
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
            TestCaseName = DBUtil.GetData(conn, "Select tc_name From test_cases Where tc_id = '%s'" % TCID, False)
            print "Running Test case id : %s :: %s" % (TCID, TestCaseName[0])
            CommonUtil.ExecLog(sModuleInfo, "-------------*************--------------", 1)
            CommonUtil.ExecLog(sModuleInfo, "Running Test case id : %s :: %s" % (TCID, TestCaseName), 1)

            #Create Log Folder for the TC
            Global.TCLogFolder = (Global.NetworkLogFolder + os.sep + sTestResultsRunId + os.sep + TCID + "_" + CommonUtil.TimeStamp("utcstring")).replace(":", "-")
            #Create the folder (this fn will delete if it already exists)
            FL.CreateFolder(Global.TCLogFolder)
            #Create sub folders needed
            FL.CreateFolder(Global.TCLogFolder + os.sep + "ProductLog")
            FL.CreateFolder(Global.TCLogFolder + os.sep + "Screenshots")


            #test Case start time
            now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)

            sTestCaseStartTime = str(now[0][0])
            iTestCaseStartTime = now[0][0]

            cur.execute("insert into test_case_results (run_id,tc_id,status,teststarttime ) values ('%s','%s','In-Progress','%s')" % (sTestResultsRunId, TCID, sTestCaseStartTime))
            conn.commit()

            #Get Test Case Index to be inserted to test_step_results table
            TestCaseResultIndex = DBUtil.GetData(conn, "Select id From test_case_results where run_id = '%s' and TC_ID = '%s' Order By id desc limit 1" % (sTestResultsRunId, TCID), False)

            #get the test case steps for this test case
            #TestStepsList = DBUtil.GetData(conn,"Select teststepname From TestSteps where TC_ID = '%s' Order By teststepsequence" %TCID,False)
            TestStepsList = DBUtil.GetData(conn, "Select ts.step_id,stepname,teststepsequence,tsl.stepsection,ts.test_step_type From Test_Steps ts,test_steps_list tsl where TC_ID = '%s' and ts.step_id = tsl.step_id Order By teststepsequence" % TCID, False)
            Stepscount = len(TestStepsList)
            sTestStepResultList = []



            #get the client name for this test case
            sClientName = TestRunID[4]

            DataSetList = DBUtil.GetData(conn, "Select tcdatasetid from test_case_datasets where tc_id='%s' and data_type='%s'" % (TCID, DataType), False) # Later we can add dataset tag like multilang here.
            if len(DataSetList) == 0:
                #This condition is for test cases which dont have any input data
                DataSetList.append('NoDataSetFound')
            for EachDataSet in DataSetList:
                #Check if this is a performance test case
                if DataType == 'Performance':
                    #this is a performance test case
                    PerfQ = Queue.Queue()
                    PerfThread = threading.Thread(target=Performance.CollectProcessMemory, args=(TestStepsList[StepSeq - 1][1], PerfQ))
                    PerfThread.start()
                    PerfQ.put('Start')
                while StepSeq <= Stepscount:
                    # Beginning of a Test Step
                    print "Step: ", TestStepsList[StepSeq - 1][1]
                    CommonUtil.ExecLog(sModuleInfo, "Step : %s" % TestStepsList[StepSeq - 1][1], 1)

                    if DataType == 'Performance':
                        PerfQ.put(TestStepsList[StepSeq - 1][1])
                    #Check if the current test step is a Performance Test Step
                    if TestStepsList[StepSeq - 1][4] == 'Performance':
                        Global.sTestStepType = TestStepsList[StepSeq - 1][4]

                    #Test Step Log id
                    Global.sTestStepExecLogId = sTestResultsRunId + TCID + str(TestStepsList[StepSeq - 1][0]) + str(StepSeq)
                    # Test Step start time
                    now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
                    sTestStepStartTime = str(now[0][0])
                    #TestStepStartTime = now[0][0]
                    TestStepStartTime = time.clock()
                    # Memory calculation at the beginning of test step
                    WinMemBegin = CommonUtil.PhysicalAvailableMemory()#MemoryManager.winmem() 
                    #update test_step_results table
                    cur.execute("insert into test_step_results (run_id,tc_id,teststep_id,teststepsequence,status,stepstarttime,logid,start_memory,testcaseresulttindex ) values ('%s','%s','%d','%d','In-Progress','%s','%s', '%s', '%d')" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], sTestStepStartTime, Global.sTestStepExecLogId, WinMemBegin, TestCaseResultIndex[0][0]))
                    conn.commit()
                    try:
                        #while True:
                            #If threading is enabled
                            #if Global.ThreadingEnabled:
                            q = Queue.Queue()
                            #Call Test Step
                            if TestStepsList[StepSeq - 1][3] == "WebDriver":
                                #If threading is enabled
                                if Global.ThreadingEnabled:
                                    stepThread = threading.Thread(target=CommonStepsDriver.ExecuteTestSteps, args=(conn, TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q))
                                else:
                                    sStepResult = Sub_Driver_Futureshop.ExecuteTestSteps(conn, TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q)

#                            elif TestStepsList[StepSeq - 1][3] == "FS":
#                                #If threading is enabled
#                                if Global.ThreadingEnabled:
#                                    stepThread = threading.Thread(target=FSDriver.ExecuteTestSteps, args=(conn, TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q))
#                                else:
#                                    sStepResult = FSDriver.ExecuteTestSteps(conn, TestStepsList[StepSeq - 1][1], TCID, sClientName, TestStepsList[StepSeq - 1][2], EachDataSet[0], q)
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
                                    sStepResult = "Critical"

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
                        print "Exception occurred in test step : ", e
                        CommonUtil.ExecLog(sModuleInfo, "Exception occurred in test step : %s" % e, 3)
                        sStepResult = "Critical"

                    #Check if the db connection is alive or timed out
                    if DBUtil.IsDBConnectionGood(conn) == False:
                        print "DB connection is bad"
                        CommonUtil.ExecLog(sModuleInfo, "DB connection error", 3)
                        try:
                            cur.close()
                        except Exception, e:
                            print "Cursor exception:", e
                            CommonUtil.ExecLog(sModuleInfo, "Exception closing DB cursor:%s" % e, 2)
                        try:
                            conn.close()
                        except Exception, e:
                            print "Connection exception:", e
                            CommonUtil.ExecLog(sModuleInfo, "Exception closing DB connection:%s" % e, 2)
                        try:
                            time.sleep(3)
                            conn = DBUtil.ConnectToDataBase()
                            cur = conn.cursor()
                        except Exception, e:
                            print "new connection exception:", e
                            CommonUtil.ExecLog(sModuleInfo, "Exception creating new DB connection:%s" % e, 2)

                    #test Step End time
                    now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
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



                    #add result of each step to a list; for a test case to pass all steps should be pass; atleast one Critical makes it 'Fail' else 'Warning' or 'Blocked'
                    if sStepResult:
                        sTestStepResultList.append(sStepResult.upper())
                    else:
                        sTestStepResultList.append("CRITICAL")
                        print "sStepResult : ", sStepResult
                        CommonUtil.ExecLog(sModuleInfo, "sStepResult : %s" % sStepResult, 1)
                        sStepResult = "Critical"

                    #Take ScreenShot
                    CommonUtil.TakeScreenShot(sStepResult + "_" + TestStepsList[StepSeq - 1][1])

                    #Update Results
                    if sStepResult.upper() == "PASS":
                        #Step Passed
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Passed"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Passed" % TestStepsList[StepSeq - 1][1], 1)
                        #Update Test Step Results table
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Pass',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                    elif sStepResult.upper() == "WARNING":
                        #Step has Warning, but continue running next test step for this test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Warning"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Warning" % TestStepsList[StepSeq - 1][1], 2)
                        #Update Test Step Results table
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Warning',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                    elif sStepResult.upper() == "CRITICAL":
                        #Step has a Critial failure, fail the test step and test case. go to next test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Critical Failure"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Critical Failure" % TestStepsList[StepSeq - 1][1], 3)
                        #Update Test Step Results table
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Critical',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        #Discontinue this test case
                        break
                    elif sStepResult.upper() == "BLOCKED":
                        #Step is Blocked, Block the test step and test case. go to next test case
                        print TestStepsList[StepSeq - 1][1] + ": Test Step Blocked"
                        CommonUtil.ExecLog(sModuleInfo, "%s : Test Step Blocked" % TestStepsList[StepSeq - 1][1], 3)
                        #Update Test Step Results table
                        DBUtil.UpdateRecordInTable(conn, 'test_step_results', "Where run_id = '%s' and tc_id = '%s' and teststep_id = '%s' and teststepsequence = '%d' and testcaseresulttindex = '%d'" % (sTestResultsRunId, TCID, TestStepsList[StepSeq - 1][0], TestStepsList[StepSeq - 1][2], TestCaseResultIndex[0][0]),
                                                   status='Blocked',
                                                   stependtime='%s' % (sTestStepEndTime),
                                                   end_memory='%s' % (WinMemEnd),
                                                   duration='%s' % (TestStepDuration),
                                                   memory_consumed='%s' % (TestStepMemConsumed)
                                                   )
                        #Discontinue this test case
                        break
                    #End Test Step
                    #increment step counter
                    StepSeq = StepSeq + 1

                    #Check if Test Set status is 'Cancelled' When it is stopped from Website
                    currentTestSetStatus = DBUtil.GetData(conn, "Select status"
                              " From test_run_env"
                              " Where run_id = '%s'" % sTestResultsRunId, False)
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
            now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
            sTestCaseEndTime = str(now[0][0])
            iTestCaseEndTime = now[0][0]

            #Decide if Test Case Pass/Failed
            if 'BLOCKED' in sTestStepResultList:
                print "Test Case Blocked"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Blocked", 3)
                sTestCaseStatus = "Blocked"
            elif 'CRITICAL' in sTestStepResultList:
                print "Test Case Failed"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Failed", 3)
                sTestCaseStatus = "Failed"
            elif 'WARNING' in sTestStepResultList:
                print "Test Case Contain Warning(s)"
                CommonUtil.ExecLog(sModuleInfo, "Test Case Contain Warning(s)", 2)
                sTestCaseStatus = "Failed"
            elif 'PASS' in sTestStepResultList:
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
            TCLogFile = CommonUtil.ZipFolder(Global.TCLogFolder, Global.TCLogFolder + ".zip")
            #Delete the folder
            FL.DeleteFolder(Global.TCLogFolder)

            #Find Test case failed reason
            try:
                FailReason = CommonUtil.FindTestCaseFailedReason(conn, sTestResultsRunId, TCID)
            except Exception, e:
                print "Unable to find Fail Reason for Test case: ", TCID
                FailReason = ""

            #Update test case result
            DBUtil.UpdateRecordInTable(conn, 'test_case_results', "Where run_id = '%s' and tc_id = '%s'" % (sTestResultsRunId, TCID), status='%s' % (sTestCaseStatus), testendtime='%s' % (sTestCaseEndTime), duration='%s' % (TestCaseDuration), failreason='%s' % (FailReason), logid='%s' % (TCLogFile))

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


                DBUtil.InsertNewRecordInToTable(conn, 'performance_results',
                        product_version=product_version,
                        tc_id=list(TestCaseID)[0],
                        run_id=sTestResultsRunId,
                        machine_os=TestRunID[4],
                        duration=Global.transaction_duration,
                        memory_avg=Global.transaction_startmemory,
                        memory_peak=Global.transaction_endmemory,
                        hw_model=hwmodel)

            #Check if Test Set status is 'Cancelled' When it is stopped from Website
            currentTestSetStatus = DBUtil.GetData(conn, "Select status"
                      " From test_run_env"
                      " Where run_id = '%s'" % sTestResultsRunId, False)
            currentTestSetStatus = currentTestSetStatus[0][0]

            if currentTestSetStatus == 'Cancelled':
                print "Test Run status is Cancelled. Exiting the current Test Set... ", sTestResultsRunId
                CommonUtil.ExecLog(sModuleInfo, "Test Run status is Cancelled. Exiting the current Test Set...%s" % sTestResultsRunId, 2)
                break


        #End of Test Set    
        #Update entry in the TestResultsEnv table that this run is completed
        #test set end time
        now = DBUtil.GetData(conn, "SELECT CURRENT_TIMESTAMP;", False)
        sTestSetEndTime = str(now[0][0])
        iTestSetEndTime = now[0][0]
        TestSetDuration = CommonUtil.FormatSeconds((iTestSetEndTime - iTestSetStartTime).seconds)

        #Update Test Run tables based on the Test Set Status
        if currentTestSetStatus == 'Cancelled':
            DBUtil.UpdateRecordInTable(conn, 'test_env_results', "Where run_id = '%s' and tester_id = '%s'" % (sTestResultsRunId, Userid), status='Cancelled', testendtime='%s' % (sTestSetEndTime), duration='%s' % (TestSetDuration))

            print "Test Set Cancelled by the User"
            CommonUtil.ExecLog(sModuleInfo, "Test Set Cancelled by the User", 1)
        else:
            DBUtil.UpdateRecordInTable(conn, 'test_env_results', "Where run_id = '%s' and tester_id = '%s'" % (sTestResultsRunId, Userid), status='Complete', testendtime='%s' % (sTestSetEndTime), duration='%s' % (TestSetDuration))

            #Update test_run_env schedule table with status so that this Test Set will not be run again
            DBUtil.UpdateRecordInTable(conn, 'test_run_env', "Where run_id = '%s' and tester_id = '%s'" % (TestRunID[0], Userid), status='Complete')
            print "Test Set Completed"
            CommonUtil.ExecLog(sModuleInfo, "Test Set Completed", 1)

            Global.sTestStepExecLogId = "MainDriver"

            #Send Summary Email
            ToEmailAddress = DBUtil.GetData(conn, "select email_notification from test_run_env where run_id = '%s'" % (TestRunID[0]), False)
            if ToEmailAddress[0][0]:
                Summary = DBUtil.GetData(conn, "select * from test_env_results where run_id = '%s'" % (TestRunID[0]), False)
                CommonUtil.SendEmail(ToEmailAddress[0][0], TestRunID[0], Summary)

        #Copy the Automation Log to Network Folder
        if FL.CopyFile(CommonUtil.hdlr.baseFilename, Global.NetworkLogFolder + os.sep + TestRunID[0].replace(':', '-')) == True:
            CommonUtil.ClearLog()

    #Close DB Connection
    conn.close

if __name__ == "__main__":

    Global.sTestStepExecLogId = "MainDriver"
    print main()



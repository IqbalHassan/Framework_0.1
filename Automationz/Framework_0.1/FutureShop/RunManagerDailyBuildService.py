import os
import psycopg2
import sys, time, datetime
import inspect
import DataBaseUtilities as DBUtil
import CommonUtil
import BuildMgr as BM
from MainDriver import main
import Cleanup
import Global
import FWUpdate

class ConfigUtil():
    _public_methods_ = ['GetConfigValue', 'SetConfigValue']
    _reg_progid_ = "ConfigUitl"

    def __init__(self):
        self.iniFile = os.path.join(os.path.dirname(__file__), 'config.ini')

    def GetConfigValue(self, sOption, sKey):
        try:
            from ConfigParser import SafeConfigParser

            parser = SafeConfigParser()
            parser.read(self.iniFile)

            return parser.get(sOption, sKey)

        except Exception, e:
            print "Exception %s" % e
            return False

    def SetConfigValue(self, sOption, sKey, sValue):
        try:
            import ConfigParser

            parser = ConfigParser.SafeConfigParser()

            parser.read(self.iniFile)
            #parser.add_section('Section1')
            parser.set(sOption, sKey, sValue)

            with open(self.iniFile, 'wb') as configfile:
                parser.write(configfile)
            return True
        except Exception, e:
            print "Exception %s" % e
            return False

def NewBuildandInstall(buildLoc, build_type, release_branch, testerid):
    #Call Build Manager
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        InstallNotifier = BM.InstallationProcessNew(buildLoc, build_type, release_branch, testerid)
        print "Build Manager has installed %s on the localhost" % InstallNotifier
        CommonUtil.ExecLog(sModuleInfo, "Install Build %s Successful" % InstallNotifier, 1)
        if "Installation done successfully. " in InstallNotifier:
            tBunInfo = InstallNotifier.partition(":")
            return tBunInfo[2]
        else:
            return False
    except Exception, e:
        print "Error in Build manager- Exception : ", e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False

def DlFormation(conn):
    print "DL"
    return Global.dl_list


def UpdateEnvParametersToDatabase(Actual_Product_Bundle, run_description):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        oCleanUp = Cleanup.CleanUp("")
        try:
            oCleanUp.DesktopCleanUp()
        except Exception, e:
            print "Exception:", e
            CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        oConfig = ConfigUtil()
        client_name = oConfig.GetConfigValue('DailyBuild', 'client_name')
        build_type = oConfig.GetConfigValue('DailyBuild', 'build_type')
        buildLoc = oConfig.GetConfigValue('DailyBuild', 'build_loc')
        test_type = run_description.replace(',', ' ')

        #Updating the test_run table in the database
        try:
            conn = DBUtil.ConnectToDataBase()
        except:
            CommonUtil.ExecLog(sModuleInfo, "DB Connection failed", 4)
            print "unable to connect to the database"

        runid = CommonUtil.TimeStamp("string")
        print "Run id is : %s" % runid

        oLocalInfo = CommonUtil.LocalInfo()
        Utesterid = oLocalInfo.getLocalUser()
        testerid = Utesterid.lower()
        machineos = oLocalInfo.getLocalOS()
        machineip = oLocalInfo.getLocalIP()
        installed_clients = oLocalInfo.getInstalledClients()
        #print installed_clients
        for eachClient in client_name.split(','):
            for eachInstallClient in installed_clients.split(','):
                if eachClient in eachInstallClient:
                    client_name = client_name.replace(eachClient, eachInstallClient)

    # 
        if run_description == 'Smoke':
            email_list = Global.dl_list

        print "Adding parameters to the test_run_env Table! "
        retVal = DBUtil.InsertNewRecordInToTable(conn, "test_run_env",
                                        run_id=runid,
                                        rundescription=run_description,
                                        test_objective=run_description,
                                        tester_id=testerid, #testerid,
                                        test_run_type="Daily_Build", #testruntype,
                                        client=client_name,
                                        machine_os=machineos,
                                        machine_ip=machineip,
                                        status='Submitted',
                                        email_notification=email_list,
                                        data_type='Default'
                                         )
        if retVal:
            conn.close()
            conVar = [testerid, runid, build_type, test_type]
            return conVar
        else:
            conn.close()
            return False
    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False

def UpdateTestSetStatus(SITestUserId):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        try:
            conn = DBUtil.ConnectToDataBase()
        except:
            print "unable to connect to the database"

        status = DBUtil.GetData(conn, "Select status from test_run_env where tester_id = '%s'" % SITestUserId)
        for eachitem in status:
            if eachitem == "In-Progress":
                DBUtil.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % SITestUserId, status="Cancelled")
                DBUtil.UpdateRecordInTable(conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % SITestUserId, status="Cancelled")
            elif eachitem == "Submitted":
                DBUtil.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % SITestUserId, status="Cancelled")
            elif eachitem == "Unassigned":
                DBUtil.DeleteRecord(conn, "test_run_env", tester_id=SITestUserId, status='Unassigned')
    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False


def PickingTestCasesOnFly(runid, name):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        try:
            conn = DBUtil.ConnectToDataBase()
        except:
            print "unable to connect to the database"
        oConfig = ConfigUtil()
        if os.name == 'nt':
            section = 'Section'
            test_run_type = 'test_run_type'
            priority = 'Priority'
            env = 'PC'
        elif os.name == 'posix':
            section = 'MacSection'
            test_run_type = 'Mac_test_run_type'
            priority = 'MacPriority'
            env = 'Mac'

        namelist = name.split(',')
        for eachname in namelist:
            if namelist.index(eachname) == 0:
                querystr = "COUNT(CASE WHEN name = '%s' and property in ('%s','%s','%s') THEN 1 END) > 0 " % (eachname, section, test_run_type, priority)
            else:
                querystr = querystr + "And COUNT(CASE WHEN name = '%s' and property in ('%s','%s','%s') THEN 1 END) > 0 " % (eachname, section, test_run_type, priority)

        OtherTestCasesIDs = DBUtil.GetData(conn, "select distinct tct.tc_id from test_case_tag tct, test_cases tc "
                    "where tct.tc_id = tc.tc_id group by tct.tc_id,tc.tc_name HAVING %s"
                    " And COUNT(CASE WHEN property = 'Ready' THEN 1 END) > 0 "
                    " And COUNT(CASE WHEN property = 'machine_os' and name = '%s' THEN 1 END) > 0"
                    " Order By tct.tc_id" % (querystr, env))

        for eachitem in OtherTestCasesIDs:
            Dict = {'run_id':runid, 'tc_id':str(eachitem)}
            Tesrt = DBUtil.InsertNewRecordInToTable(conn, "test_run", **Dict)
    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False

def ResAnalysis(testerid, conn, runid, build, build_type, release_branch, Path):
    print "Result Analysis"
    CriticalCount = 1
    PartialCount = 1
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        TestResults = DBUtil.GetData(conn, "Select tc_id,status From test_case_results Where run_id='%s'" % runid, False)
        for eachitem in TestResults:
            PropVal = DBUtil.GetData(conn, "Select name From test_case_tag Where tc_id='%s' and property='Acceptance'" % eachitem[0], False)
            if len(PropVal) > 0:
                if PropVal[0][0] == 'Critical':
                    if eachitem[1] != 'Passed':
                        #print eachitem[0] + ": Did not pass"
                        CriticalCount = 0
            else:
                if eachitem[1] != 'Passed':
                    #print eachitem[0] + ": Did not pass"
                    PartialCount = 0
        if CriticalCount == 0:
            print "SI did not pass"
            #BM.UpdateBuildStatusDB(testerid, "SI did not pass", build, "Insert", build_type, release_branch, runid, Path)
        elif CriticalCount == 1 and PartialCount == 0:
            print "SI passed with partial success"
            #BM.UpdateBuildStatusDB(testerid, "SI passed with partial success", build, "Insert", build_type, release_branch, runid, Path)
        else:
            print "SI successful"
            #BM.UpdateBuildStatusDB(testerid, "SI Successful", build, "Insert", build_type, release_branch, runid, Path)  
    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return "Error in result analysis"

def RunProcessNew(buildLoc, build_type, release_branch, testerid):
    try:
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        build = False
        build = NewBuildandInstall(buildLoc, build_type, release_branch, testerid)

        #Reads the Config file for the environment parameters to the run AND update SI Test
        if not(build) == False:
            oConfig = ConfigUtil()
            RunNameStr = oConfig.GetConfigValue('DailyBuild', 'name')
            client_name = oConfig.GetConfigValue('DailyBuild', 'client_name')
            RunNameList = filter(None, [x.strip() for x in RunNameStr.splitlines()])
            for eachRunName in RunNameList:
                try:
                    conn = DBUtil.ConnectToDataBase()
                except:
                    print "unable to connect to the database"

                conVarList = UpdateEnvParametersToDatabase(build, eachRunName)
                testerid = conVarList[0]
                runid = conVarList[1]
                build_type = conVarList[2]
                test_type = conVarList[3]
                PickingTestCasesOnFly(runid, eachRunName)
                DlList = DlFormation(conn)
                if os.name == 'nt':
                    if build_type == 'TestBuild':
                        buildDetails = "Branch:" + build_type + ",Bundle:" + build
                    else:
                        buildDetails = "Branch:" + build_type + ",Bundle:" + build
                elif os.name == 'posix':
                    buildDetails = "Branch:" + build_type + ",Bundle:" + build
                DBUtil.UpdateRecordInTable(conn, 'test_run_env', "Where run_id = '%s'" % runid, product_version=buildDetails)

                if build_type == 'TestBuild':
                    if os.name == 'nt':
                        Path = "//ServerLocation/" + release_branch + '/' + build
                    elif os.name == 'posix':
                        Path = "//ServerLocation/" + release_branch + '/' + build
                else:
                    Path = buildLoc + "/job/" + build_type + "/" + build

                status = DBUtil.GetData(conn, "Select status from test_run_env where run_id = '%s'" % runid)
                if status[0] == "Submitted":
                    ############################### UPDATE THE STATUS TO RUNNING THE TEST CASES
                    BM.UpdateBuildStatusDB(testerid, "SI test cases running", build, "Insert", build_type, release_branch, runid, Path)
                    BM.UpdateBuildStatusDB(testerid, "Running", build, "Insert", build_type, release_branch, "N/A", "N/A")
                    print "Sending email"
                    #Start Email List
                    StartEmailList = "test@test.com"
                    CommonUtil.SendEmail(StartEmailList, runid, buildDetails, "Daily_Build")
                    print "Calling the MainDriver"
                    main()
                    ############################### TEST CASES DONE
                    BM.UpdateBuildStatusDB(testerid, "SI test cases finished", build, "Insert", build_type, release_branch, runid, Path)
                    BM.UpdateBuildStatusDB(testerid, "Completed", build, "Insert", build_type, release_branch, "N/A", "N/A")

                    # Result Analysis
                    ResAnalysis(testerid, conn, runid, build, build_type, release_branch, Path)

    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog(sModuleInfo, "Exception:%s" % e, 4)
        return False

#Call the Python Driver to execute the test run
if __name__ == '__main__':
    oConfigVal = ConfigUtil()
    oTestInfo = CommonUtil.LocalInfo()
    buildLoc = oConfigVal.GetConfigValue('DailyBuild', 'build_loc')
    build_type = oConfigVal.GetConfigValue('DailyBuild', 'build_type')
    release_branch = oConfigVal.GetConfigValue('DailyBuild', 'release_branch')
    frequency = int(oConfigVal.GetConfigValue('DailyBuild', 'frequency')) #5  no. of times build should be checked
    startTime = oConfigVal.GetConfigValue('DailyBuild', 'start_time') #3  provide start time in 24 hrs clock
    testerid = oTestInfo.getLocalUser().lower()
    try:
        if os.name == 'posix':
            import BuildMgr as BM
            #Mount Automation folder
            if BM.MountDrive('/Volumes/AutomationDrive', '//NetworkPath/Folder'):
                print "Successfully mounted automation folder"
            else:
                print "Failed to mount automation folder"

        else:
            if CommonUtil.mapNetworkDrive('s:', "\\\\NetworkPath\Folder"):
                print "Framework drive is mapped/accessible"
            else:
                print "Error in accessing / mapping framework drive. Map the drive manually and run again!!!"

        #Check if there is a FW update available
        objFW = FWUpdate.AutoUpdate()
        if objFW.UpdateProcess() == 'restart':
            os.execl (sys.executable, sys.executable, *sys.argv)

    except Exception, e:
        print "Exception %s" % e
        CommonUtil.ExecLog("Main", "Exception:%s" % e, 4)
        print "Error in build manager. After initial work around"

    UpdateTestSetStatus(testerid)
    test_type = ""
    TimeToCheck = []
    try:
        if frequency <> -1:
            if 24 % frequency == 0:
                eqInterval = 24 / frequency
                print "Smoke test will run " + str(frequency) + " times a day"
                test_type = 'Prod'
            else:
                print "Frequency is not in acceptable list. It should be either [1,2,3,4,6,12]"
        else:
            test_type = 'Dev'

    except:
        print "unable to connect to the database"
    e = 0
    if test_type == 'Prod':
        while e < frequency:
            addTimeToList = startTime + (eqInterval * e)
            if addTimeToList >= 24:
                addTimeToList = addTimeToList - 24
            TimeToCheck.append(addTimeToList)
            e = e + 1
        RunAgain = True
        while RunAgain == True:
            now = datetime.datetime.now()
            hr = (now.hour)
            for eachElement in TimeToCheck:
                if eachElement == hr:
                    BM.UpdateBuildStatusDB(testerid, "Build check procedure in place", "N/A", "Insert", build_type, release_branch, "N/A", "N/A")
                    RunProcessNew(buildLoc, build_type, release_branch, testerid)
                    #################### WAITING FOR A NEW BUILD. BUILD LAST CHECKED AT TIME
                    BM.UpdateBuildStatusDB(testerid, "Waiting for a new build", "N/A", "Update", build_type, release_branch, "N/A", "N/A")
    elif test_type == 'Dev':
        RunAgain = True
        while RunAgain == True:
            #BM.UpdateBuildStatusDB(testerid, "Build check procedure in place", "N/A", "Insert",build_type,release_branch, "N/A", "N/A")
            RunProcessNew(buildLoc, build_type, release_branch, testerid)
            #################### WAITING FOR A NEW BUILD. BUILD LAST CHECKED AT TIME
            BM.UpdateBuildStatusDB(testerid, "Waiting for a new build", "N/A", "Update", build_type, release_branch, "N/A", "N/A")
            time.sleep(360)




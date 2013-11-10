import os
import psycopg2
import DataBaseUtilities as DBUtil
import CommonUtil
import FileUtilities as FileUtil
import sys, time, datetime
import Global
import Cleanup
import FWUpdate


def UpdateEnvParametersToDatabase():
    print "Updating Database with Environment information"

    try:

        #Clean up Log File
        oCleanUp = Cleanup.CleanUp("")

        try:
            oCleanUp.DesktopCleanUp()
        except Exception, e:
            print "Exception:", e

        #Get Local Info object
        oLocalInfo = CommonUtil.LocalInfo()

        #Check Network Access
        if os.path.isdir(Global.NetworkFolder) != True:
            print "Failed to access Network folder"
            #return False
            local_ip = oLocalInfo.getLocalIP() + " - Network Error"
        else:
            local_ip = oLocalInfo.getLocalIP()


        testerid = (oLocalInfo.getLocalUser()).lower()
        product_version = ''
        machine_os = oLocalInfo.getLocalOS()

        #Client Info
        client = oLocalInfo.getInstalledClients()

        UpdatedTime = CommonUtil.TimeStamp("integer")

        #Updating the test_run table in the database
        try:
            conn = DBUtil.ConnectToDataBase()
        except:
            print "unable to connect to the database"

        #runid = TimeStamp()
        status = DBUtil.GetData(conn, "Select status from test_run_env where tester_id = '%s'" % testerid)
        for eachitem in status:
            if eachitem == "In-Progress":
                DBUtil.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
                DBUtil.UpdateRecordInTable(conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
            elif eachitem == "Submitted":
                DBUtil.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % testerid, status="Cancelled")
            elif eachitem == "Unassigned":
                DBUtil.DeleteRecord(conn, "test_run_env", tester_id=testerid, status='Unassigned')


        print "Adding parameters to the test_run_env Table! "
        test_run_env = DBUtil.InsertNewRecordInToTable(conn, "test_run_env",

                                        tester_id=testerid,
                                        product_version=str(product_version),
                                        machine_os=machine_os,
                                        machine_ip=local_ip,
                                        client=client,
                                        status="Unassigned",
                                        data_type="Default",
                                        last_updated_time=UpdatedTime
                                         )
        if test_run_env == True:
            conn.close()
            return testerid
        else:
            print "Failed to Add parameters to the test_run_env Table! :", test_run_env
            conn.close()
            return False
    except Exception, e:
        print "Exception:", e
        return False
def RunProcess(sTesterid):

    while (1):
        try:
            conn = DBUtil.ConnectToDataBase()
            status = DBUtil.GetData(conn, "Select status from test_run_env where tester_id = '%s' and status in ('Submitted','Unassigned') limit 1 " % (sTesterid))
            conn.close()
            if len(status) == 0:
                continue
            if status[0] != "Unassigned":
                if status[0] == "Submitted":
                    import MainDriver
                    MainDriver.main()
                    print "updating db with parameter"
                    UpdateEnvParametersToDatabase()
                    print "Successfully updated db with parameter"

            elif status[0] == "Unassigned":
                time.sleep(3)
                conn = DBUtil.ConnectToDataBase()
                DBUtil.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Unassigned'" % sTesterid, last_updated_time=CommonUtil.TimeStamp("integer"))
                conn.close()
                #Check if there is any fw update
#                objFW = FWUpdate.AutoUpdate()
#                if objFW.UpdateProcess() == 'restart':
#                    os.execl (sys.executable, sys.executable, *sys.argv)

        except Exception, e:
            print "Exception : ", e

    return "Continue"


if __name__ == '__main__':

#        if os.name == 'posix':
#            import BuildMgr as BM
#            #Mount Automation folder
#            if BM.MountDrive('/Volumes/AutomationDrive', '//NetworkPath/Folder'):
#                print "Successfully mounted automation folder"
#            else:
#                print "Failed to mount automation folder"
#
#        else:
#            if CommonUtil.mapNetworkDrive('s:', "\\\\NetworkPath\Folder"):
#                print "Framework drive is mapped/accessible"
#            else:
#                print "Error in accessing / mapping framework drive. Map the drive manually and run again!!!"


        #Check if there is a FW update available
        objFW = FWUpdate.AutoUpdate()
        if objFW.UpdateProcess() == 'restart':
            os.execl (sys.executable, sys.executable, *sys.argv)


        GivemeTesterID = UpdateEnvParametersToDatabase()
        if GivemeTesterID != False:
            RunAgain = RunProcess(GivemeTesterID)
            if RunAgain == True:
                UpdateEnvParametersToDatabase()



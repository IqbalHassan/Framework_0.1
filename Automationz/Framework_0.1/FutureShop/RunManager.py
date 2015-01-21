import DataBaseUtilities as DB
from dependencyCollector import dependency,product_version
import Cleanup
from login_info import username,password,project,team,server,port,database_name,superuser,super_password
import CommonUtil
import os
import Global
import time
import MainDriver
def RunProcess(sTesterid):
    while (1):
        try:
            conn = DB.ConnectToDataBase()
            status = DB.GetData(conn, "Select status from test_run_env where tester_id = '%s' and status in ('Submitted','Unassigned') limit 1 " % (sTesterid))
            conn.close()
            if len(status) == 0:
                continue
            if status[0] != "Unassigned":
                if status[0] == "Submitted":
                    value=MainDriver.main()
                    print "updating db with parameter"
                    if value=="pass":
                        break
                    print "Successfully updated db with parameter"

            elif status[0] == "Unassigned":
                time.sleep(3)
                conn = DB.ConnectToDataBase()
                last_updated_time=CommonUtil.TimeStamp("string")
                DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Unassigned'" % sTesterid, last_updated_time=last_updated_time)
                conn.close()
        except Exception, e:
            print "Exception : ", e

    return True

def Login():
    print username
    result=Check_Credentials(username,password,project,team,server,port)
    if result:
        tester_id=update_machine(collectAlldependency(project,team,dependency))
        if tester_id!=False:
            RunAgain = RunProcess(tester_id)
            if RunAgain == True:
                Login()
        else:
            print "machine not generated"
    else:
        print "No User Found"

def collectAlldependency(project,team_info,dependency):
    query="select distinct dependency_name from dependency d ,dependency_management dm where d.id=dm.dependency and dm.project_id='%s' and dm.team_id=(select id from config_values where value='%s' and type='Team')"%(project,team_info)
    print query
    Conn=DB.ConnectToDataBase(database_name, superuser, super_password, server)
    dependency_list=DB.GetData(Conn, query)
    Conn.close()
    print dependency_list

    #Get Local Info object
    oLocalInfo = CommonUtil.LocalInfo()

    final_dependency=[]
    for each in dependency_list:
        temp=""
        temp_list=[]
        if each in dependency.keys():
            if dependency[each]!='':
                temp=dependency[each]
            else:
                if each=='Platform':
                    temp=oLocalInfo.getLocalOS()
                if each=='Browser':
                    temp=oLocalInfo.getInstalledClients()
        else:
            if each=='Platform':
                temp=oLocalInfo.getLocalOS()
            if each=='Browser':
                temp=oLocalInfo.getInstalledClients()
        if temp!='':
            if each=='Platform':
                bit=int(temp.split('-')[1].strip()[0:2])
                version=temp.split('-')[0].split(' ')[1].strip()
                name=temp.split('-')[0].split(' ')[0].strip()
                temp_list.append((name,bit,version))
            if each=='Browser':
                temp=temp.split(",")
                for eachitem in temp:
                    bit=int(eachitem.split(";")[1].strip()[0:2])
                    version=eachitem.split(";")[0].split("(")[1].split("V")[1].strip()
                    name=eachitem.split(";")[0].split("(")[0].strip()
                    temp_list.append((name,bit,version))
            if each=='TestCaseType':
                temp_list.append((temp,0,''))
            final_dependency.append((each,temp_list))
    return final_dependency

def update_machine(dependency):
    try:
        #Get Local Info object
        oLocalInfo = CommonUtil.LocalInfo()

        if os.path.isdir(Global.NetworkFolder) != True:
            print "Failed to access Network folder"
            #return False
            local_ip = oLocalInfo.getLocalIP() + " - Network Error"
        else:
            local_ip = oLocalInfo.getLocalIP()
        testerid = (oLocalInfo.getLocalUser()).lower()
        #product_version = ' '        
        productVersion=product_version
        UpdatedTime = CommonUtil.TimeStamp("string")
        query="select count(*) from permitted_user_list where user_level='Automation' and user_names='%s'"%testerid
        Conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
        count=DB.GetData(Conn,query)
        Conn.close()
        if isinstance(count,list) and count[0]==0:
            #insert to the permitted_user_list
            temp_Dict={
                'user_names':testerid,
                'user_level':'Automation',
                'email':testerid+"@machine.com"
            }
            Conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
            result=DB.InsertNewRecordInToTable(Conn,"permitted_user_list",**temp_Dict)
            Conn.close()
            
        #update the test_run_env table
        dict={
            'tester_id':testerid,
            'status':'Unassigned',
            'last_updated_time':UpdatedTime,
            'machine_ip':local_ip,
            'branch_version':productVersion
        }
        conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
        status = DB.GetData(conn, "Select status from test_run_env where tester_id = '%s'" % testerid)
        conn.close()
        for eachitem in status:
            if eachitem == "In-Progress":
                conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
                DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
                conn.close()
                conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
                DB.UpdateRecordInTable(conn, "test_env_results", "where tester_id = '%s' and status = 'In-Progress'" % testerid, status="Cancelled")
                conn.close()
            elif eachitem == "Submitted":
                conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
                DB.UpdateRecordInTable(conn, "test_run_env", "where tester_id = '%s' and status = 'Submitted'" % testerid, status="Cancelled")
                conn.close()
            elif eachitem == "Unassigned":
                conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
                DB.DeleteRecord(conn, "test_run_env", tester_id=testerid, status='Unassigned')
                conn.close()
        conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
        result=DB.InsertNewRecordInToTable(conn,"test_run_env",**dict)
        conn.close()
        if result:
            conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
            machine_id=DB.GetData(conn,"select id from test_run_env where tester_id='%s' and status='Unassigned'"%testerid)
            conn.close()
            if isinstance(machine_id,list) and len(machine_id)==1:
                machine_id=machine_id[0]
            for each in dependency:
                type_name=each[0]
                listings=each[1]
                for eachitem in listings:
                    temp_dict={
                        'name':eachitem[0],
                        'bit':eachitem[1],
                        'version':eachitem[2],
                        'type':type_name,
                        'machine_serial':machine_id
                    }
                    conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
                    result=DB.InsertNewRecordInToTable(conn,"machine_dependency_settings",**temp_dict)
                    conn.close()
            conn=DB.ConnectToDataBase(database_name, superuser,super_password,server)
            teamValue=DB.GetData(conn,"select id from config_values where value='%s' and type='Team'"%team)
            conn.close()
            if isinstance(teamValue,list) and len(teamValue)==1:
                team_identity=teamValue[0]
            temp_dict={
                'machine_serial':machine_id,
                'project_id':project,
                'team_id':team_identity
            }
            conn=DB.ConnectToDataBase(database_name, superuser,super_password,server)
            result=DB.InsertNewRecordInToTable(conn,"machine_project_map",**temp_dict)
            conn.close()
            if result:
                return testerid
        return False
    except Exception, e:
        print "Exception:",e
    
def Check_Credentials(username,password,project,team,server,port):
    #get all the person enlisted with this project
    query="select regexp_split_to_array(project_owners, E',') from projects where project_id='%s'"%project
    Conn=DB.ConnectToDataBase(database_name, superuser, super_password, server)
    user_list=DB.GetData(Conn, query)
    Conn.close()
    user_list=user_list[0]
    message=",".join(user_list)
    print message
    query="select count(*) from user_info ui, permitted_user_list pul where ui.full_name=pul.user_names and username='%s' and password='%s' and user_level not in ('email','Automation', 'Manual') and user_id in (%s)"%(username,password,message)
    Conn=DB.ConnectToDataBase(database_name,superuser,super_password,server)
    count=DB.GetData(Conn,query)
    Conn.close()
    print count
    if len(count)==1 and count[0]==1:
       return True 
    else:
        print "No user found with Name: %s"%username
        return False
if __name__=='__main__':
    Login()
import time
Enviroment='Production'
Enviroment='Development'

user='postgres'
password_user='password'
db_name='postgres'

if Enviroment=='Production':
    server='135.23.123.206'

if Enviroment=='Development':
    server='127.0.0.1'

import DataBaseUtilities as DB
import EmailNotify
import urllib2

def main():
    while(1):
        Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
        query="select run_id,email_notification,email_flag from test_run_env where email_flag=true"
        pending_item=DB.GetData(Conn,query,False)
        Conn.close()
        #print pending_item
        for each in pending_item:
            result=Send_Report(each[0], each[1])
            if result:
                Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
                sWhereQuery="where run_id='%s'"%(each[0])
                print DB.UpdateRecordInTable(Conn,'test_run_env',sWhereQuery,email_flag=False)
        time.sleep(15)
        print "recheck for pending items"
        
def Send_Report(run_id,stEmailIds):
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
    status = DB.GetData(Conn,"select status from test_run_env where run_id = '" +run_id +"'")
    Conn.close()
    
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    TestObjective = DB.GetData(Conn,"select test_objective from test_run_env where run_id = '" +run_id +"'")
    Conn.close()
    
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    Tester = DB.GetData(Conn,"select assigned_tester from test_run_env where run_id = '" +run_id +"'")
    Conn.close()
    
    list = []
    
    pass_query = "select count(*) from test_case_results where run_id='%s' and status='Passed'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    passed = DB.GetData(Conn, pass_query)
    Conn.close()
    list.append(passed[0])
    
    fail_query = "select count(*) from test_case_results where run_id='%s' and status='Failed'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    fail = DB.GetData(Conn, fail_query)
    Conn.close()
    list.append(fail[0])
    
    blocked_query = "select count(*) from test_case_results where run_id='%s' and status='Blocked'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    blocked = DB.GetData(Conn, blocked_query)
    Conn.close()
    list.append(blocked[0])
    
    progress_query = "select count(*) from test_case_results where run_id='%s' and status='In-Progress'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    progress = DB.GetData(Conn, progress_query)
    Conn.close()
    list.append(progress[0])
    
    submitted_query = "select count(*) from test_case_results where run_id='%s' and status='Submitted'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    submitted = DB.GetData(Conn, submitted_query)
    Conn.close()
    list.append(submitted[0])
    
    skipped_query = "select count(*) from test_case_results where run_id='%s' and status='Skipped'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    skipped = DB.GetData(Conn, skipped_query)
    Conn.close()
    list.append(skipped[0])
    
    total_query = "select count(*) from test_case_results where run_id='%s'" % run_id
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    total = DB.GetData(Conn, total_query)
    Conn.close()
    list.append(total[0])
    
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)    
    duration = DB.GetData(Conn,"select to_char(now()-teststarttime,'HH24:MI:SS') as Duration from test_env_results where run_id = '" + run_id +"'")
    Conn.close()
    
    try:
        urllib2.urlopen("http://www.google.com").close()
        #import EmailNotify
        EmailNotify.Pending_Email(stEmailIds,run_id,str(TestObjective[0]),status[0],list,Tester,duration,'','')
        print "connected"
        return True
    except urllib2.URLError:
        print "disconnected"
        return False
if __name__=='__main__':
    main()
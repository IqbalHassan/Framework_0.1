import time
import Global
import requests
import socket
from datetime import datetime, timedelta
user='postgres'
password_user='password'
db_name='postgres'
server=Global.get_ip()
port=Global.get_port()
import DataBaseUtilities as DB
import EmailNotify
import urllib2
import threading
def main():
    email_thread = threading.Thread(name='email_service', target=send,args=(60,))
    email_thread.start()
    schedule_run_thread=threading.Thread(name='scheduled_run_service',target=schedule_run,args=(60,))
    schedule_run_thread.start()
def schedule_run(timediff):
    print threading.current_thread().getName()+' starting'
    while(1):
        query="select distinct schedule,run_time,run_day from schedule"
        Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
        schedule_list=DB.GetData(Conn,query,False)
        print schedule_list
        Conn.close()
        for each in schedule_list:
            run_tag=False
            current_time_date=datetime.now()            
            if each[2] in ['All','Fiv','Ten','Thi','One']:
                current_time=current_time_date.strftime("%H:%M")
                if each[1].strip()==current_time:
                    run_tag=True
            else:
                current_time=current_time_date.strftime("%H:%M/%a")
                if each[1].strip()+'/'+each[2].strip()==current_time:
                    run_tag=True
            if run_tag:
                query="select schedule,run_test_query,dependency,machine,testers,email,milestone,testObjective,project_id,team_id from schedule where schedule=%d"%int(each[0])
                Conn=DB.ConnectToDataBase(db_name,user, password_user, server)
                run_detail=DB.GetData(Conn,query,False)
                print run_detail
                Conn.close()
                run_query=run_detail[0][1]+run_detail[0][2]
                machine_query=run_detail[0][3]
                tester_id=run_detail[0][4].split(",")
                tester_id="|".join(tester_id)
                email_id=run_detail[0][5].split(",")
                email_id="|".join(tester_id)
                milestone=run_detail[0][6]
                testobjective=run_detail[0][7]
                project_id=run_detail[0][8]
                team_id=run_detail[0][9]
                start_date=''
                end_date=''
                url='http://'+server+":"+str(port)+'/Home/RunTest/Run_Test'
                kwarg_list={
                    'RunTestQuery': run_query+machine_query,
                    'TesterIds':tester_id,
                    'EmailIds':email_id,
                    'TestObjective':testobjective,
                    'TestMileStone':milestone,
                    'project_id':project_id,
                    'team_id':team_id,
                }
                if each[2]=='Fiv':
                    difference=5
                elif each[2]=='Ten':
                    difference=10
                elif each[2]=='Thi':
                    difference=30
                elif each[2]=='One':
                    difference=60
                else:
                    difference=0
                next_time_string=(datetime.strptime(each[1], "%H:%M")+timedelta(minutes=int(difference))).strftime("%H:%M")
                sWhereQuery="where schedule=%d"%int(each[0])
                Conn=DB.ConnectToDataBase(db_name, user, password_user, server)
                print DB.UpdateRecordInTable(Conn, "schedule", sWhereQuery,run_time=next_time_string.strip())
                Conn.close()
                try:
                    r=requests.get(url,params=kwarg_list)
                    print r.url
                except:
                    print "exception handled"   
        time.sleep(timediff)
        print "waiting for scheduled run.."
def send(timediff):
    print threading.current_thread().getName()+' starting\n'
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
        time.sleep(timediff)
        print "waiting...."
        
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
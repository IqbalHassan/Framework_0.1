from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
import datetime
import inspect
def testConnection(Conn):
    if DB.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()

def CreateNewBug(title,status,description,start_date,end_date,team,priority,milestone,project_id,user_name,creator,testers):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        Conn=GetConnection()
        query="select nextval('bugid_seq')"
        bug_id=DB.GetData(Conn, query)
        bug_id=('BUG-'+str(bug_id[0]))
        bug_id=bug_id.strip()
        testConnection(Conn)
        print 'aissala'
        
        #get the current time and date
        now=datetime.datetime.now().date()
        #now form a directory to send the other information
        Dict={
              'bug_id':bug_id,
              'bug_title':title,
              'bug_description':description,
              'bug_startingdate':start_date,
              'bug_endingdate':end_date,
              'bug_priority':priority,
              'bug_milestone':milestone,
              'bug_createdby':creator,
              'bug_creationdate':now,
              'bug_modifiedby':user_name,
              'bug_modifydate':now,
              'status':status,
              'team_id':team,
              'project_id':project_id,
              'tester':testers
        }
        testConnection(Conn)
        result = DB.InsertNewRecordInToTable(Conn,"bugs",**Dict)
        #result = DB.InsertNewRecordInToTable(Conn, "bugs", bug_id=bug_id, bug_title=title, bug_description=description, bug_startingdate=start_date, bug_endingdate=end_date,bug_priority=priority, bug_milestone=milestone, bug_createdby=creator, bug_creationdate=now, bug_modifiedby=user_name, bug_modifydate=now, status=status, tester=testers, team_id=team, project_id=project_id)
        if result==True:
            #add this line in the code from LogModule import PassMessage
            #log message successful here 
            #message format be PassMessage(sModuleInfo, message,1 for pass,2 for warning, 3 for error,debug=True)
            #PassMessage(sModuleInfo,"Inserted "+bug_id+" successfully", 1)
            return bug_id
        else:
            return 'meh'
        """if result==True:
            for each in teams:
                #form new Dict
                team_dict={
                    'bug_id':bug_id,
                    'team_id':each
                }
                testConnection(Conn)
                result=DB.InsertNewRecordInToTable(Conn,"bug_team_map",**team_dict)
                if result==False:
                    return False
            return bug_id"""
        #register another path for the bug to be grabbed by the buguirement
        #register this bug in the bug_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
import datetime
def testConnection(Conn):
    if DB.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()

def CreateNewBug(title,status,description,start_date,end_date,team,priority,milestone,project_id,user_name,creator,testers):
    try:
        Conn=GetConnection()
        query="select nextval('bugid_seq')"
        bug_id=DB.GetData(Conn, query)
        bug_id=('BUG-'+str(bug_id[0]))
        bug_id=bug_id.strip()
        testConnection(Conn)
        
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
              'tester':testers,
              'team_id':team,
              'project_id':project_id
        }
        testConnection(Conn)
        #result=DB.InsertNewRecordInToTable(Conn,"bugs",**Dict)
        result = DB.InsertNewRecordInToTable(Conn, "bugs", bug_id=bug_id, bug_title=title, bug_description=description, bug_startingdate=start_date, bug_endingdate=end_date,bug_priority=priority, bug_milestone=milestone, bug_createdby=creator, bug_creationdate=now, bug_modifiedby=user_name, bug_modifydate=now, status=status, tester=testers, team_id=team, project_id=project_id)
        return bug_id
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
        
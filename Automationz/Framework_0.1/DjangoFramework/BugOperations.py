from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
import datetime
import inspect
import LogModule
from LogModule import PassMessasge
def testConnection(Conn):
    if DB.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()

def CreateNewBug(title,status,description,start_date,end_date,team,priority,milestone,project_id,user_name,testers,test_cases,labels,Feature_Path):
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
              'bug_createdby':user_name,
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
        
        if test_cases[0] != '':
            for each in test_cases:
                cases_Dict={
                           'id1':bug_id,
                           'id2':each.strip(),
                           'type1':'BUG',
                           'type2':'TC'
                }
                new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
                
        if labels[0] != '':
            for each in labels:
                label_Dict={
                           'lm_id':bug_id,
                           'label_id':each.strip(),
                           'type':'BUG'
                }
                hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
        #result = DB.InsertNewRecordInToTable(Conn, "bugs", bug_id=bug_id, bug_title=title, bug_description=description, bug_startingdate=start_date, bug_endingdate=end_date,bug_priority=priority, bug_milestone=milestone, bug_createdby=creator, bug_creationdate=now, bug_modifiedby=user_name, bug_modifydate=now, status=status, tester=testers, team_id=team, project_id=project_id)
        
        Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % Feature_Path)
        if len(Feature_Id) > 0:
            feat_Dict={
                           'fm_id':bug_id,
                           'type':'BUG',
                           'feature_id':Feature_Id[0]
                }
            fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
            feat = Feature_Path.split('.')
        """level = 1
        eachFeature = DB.GetData(Conn,"select subpath(feature_path,0,"+level+") from product_features where feature_path = '"+Feature_Path+"'")
        while eachFeature != Feature_Path:
            Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % eachFeature[0])
            feat_Dict={
                       'id':bug_id,
                       'type':'BUG',
                       'feature_id':Feature_Id[0]
            }
            fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
            level = level + 1
            eachFeature = DB.GetData(Conn,"select subpath(feature_path,0,"+level+") from product_features where feature_path = '"+Feature_Path+"'")
        """
        
        if result==True:
            #add this line in the code from LogModule import PassMessage
            #log message successful here 
            #message format be PassMessage(sModuleInfo, message,1 for pass,2 for warning, 3 for error,debug=True)
            LogModule.PassMessasge(sModuleInfo,"Inserted "+bug_id+" successfully", 1)
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
        
        
def EditBug(bug_id,title,status,description,start_date,end_date,team,priority,milestone,project_id,user_name,testers,test_cases,labels,Feature_Path):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
    try:
        Conn=GetConnection()
        """query="select nextval('bugid_seq')"
        bug_id=DB.GetData(Conn, query)
        bug_id=('BUG-'+str(bug_id[0]))
        bug_id=bug_id.strip()"""
        testConnection(Conn)
        print 'jassala'
        
        #get the current time and date
        now=datetime.datetime.now().date()
        #now form a directory to send the other information
        condition = "where bug_id='%s'" % bug_id
        Dict={
              'bug_id':bug_id,
              'bug_title':title,
              'bug_description':description,
              'bug_startingdate':start_date,
              'bug_endingdate':end_date,
              'bug_priority':priority,
              'bug_milestone':milestone,
              #'bug_createdby':user_name,
              #'bug_creationdate':now,
              'bug_modifiedby':user_name,
              'bug_modifydate':now,
              'status':status,
              'team_id':team,
              'project_id':project_id,
              'tester':testers
        }
        testConnection(Conn)
        result = DB.UpdateRecordInTable(Conn,"bugs", condition, **Dict)
        
        if test_cases[0] != '':
            tcres=DB.DeleteRecord(Conn, "components_map", id1=bug_id, type1='BUG', type2='TC')
            for each in test_cases:
                cases_Dict={
                           'id1':bug_id,
                           'id2':each.strip(),
                           'type1':'BUG',
                           'type2':'TC'
                }
                new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
                
        if labels[0] != '':
            lsres=DB.DeleteRecord(Conn,"label_map", lm_id=bug_id)
            for each in labels:
                label_Dict={
                           'lm_id':bug_id,
                           'label_id':each.strip(),
                           'type':'BUG'
                }
                hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
        
        
        #result = DB.InsertNewRecordInToTable(Conn, "bugs", bug_id=bug_id, bug_title=title, bug_description=description, bug_startingdate=start_date, bug_endingdate=end_date,bug_priority=priority, bug_milestone=milestone, bug_createdby=creator, bug_creationdate=now, bug_modifiedby=user_name, bug_modifydate=now, status=status, tester=testers, team_id=team, project_id=project_id)
        
        Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % Feature_Path)
        if len(Feature_Id) > 0:
            lsres=DB.DeleteRecord(Conn,"feature_map", fm_id=bug_id)
            feat_Dict={
                           'fm_id':bug_id,
                           'type':'BUG',
                           'feature_id':Feature_Id[0]
                }
            fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)

        
        if result==True:
            #add this line in the code from LogModule import PassMessage
            #log message successful here 
            #message format be PassMessage(sModuleInfo, message,1 for pass,2 for warning, 3 for error,debug=True)
            LogModule.PassMessasge(sModuleInfo,"Modified "+bug_id+" successfully", 1)
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
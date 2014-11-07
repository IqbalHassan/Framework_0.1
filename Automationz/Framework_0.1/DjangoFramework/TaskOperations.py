from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
import datetime
def testConnection(Conn):
    if DB.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
def insert_new_section(Conn,new_requirement_path):
    query="select max(requirement_path_id) from requirement_sections"
    testConnection(Conn)
    sequence_number=DB.GetData(Conn,query)
    if isinstance(sequence_number,list) and len(sequence_number)==1:
        if sequence_number[0] is None:
            sequence=1
        else:
            sequence=int(sequence_number[0])+1
    query="insert into requirement_sections(requirement_path_id,requirement_path) values('%s','%s')"%(sequence,new_requirement_path)
    cur=Conn.cursor()
    cur.execute(query)
    cur.close()
    Conn.commit()
    return sequence
        
def CreateNewTask(title,status,description,start_date,end_date,teams,tester,priority,milestone,project_id,section_path,feature_path,user_name):
    try:
        Conn=GetConnection()
        query="select nextval('taskid_seq')"
        testConnection(Conn)
        task_id=DB.GetData(Conn,query)
        if isinstance(task_id,list) and len(task_id)==1:
            task_id=int(task_id[0])+1
            task_id=str('TASK-'+str(task_id))
        
        if section_path=="No_Parent":
            new_requirement_path=task_id.replace('-', '_')
            path_id=insert_new_section(Conn, new_requirement_path)
        else:
            query="select requirement_path_id,requirement_path from requirement_sections where requirement_path ~'%s'"%(section_path.replace('-', '_'))
            requirement_path=DB.GetData(Conn,query,False)
            if isinstance(requirement_path,list) and len(requirement_path)==1:
                path_id=requirement_path[0][0]
                path=requirement_path[0][1]
                new_requirement_path=path+"."+(task_id).replace('-','_')
                sequence=insert_new_section(Conn,new_requirement_path.strip())
        #get the current time and date
        now=datetime.datetime.now().date()
        #now form a directory to send the other information
        Dict={
              'tasks_id':task_id,
              'tasks_title':title,
              'tasks_description':description,
              'tasks_startingdate':start_date,
              'tasks_endingdate':end_date,
              'tasks_createdby':user_name,
              'tasks_creationdate':now,
              'tasks_modifiedby':user_name,
              'tasks_modifydate':now,
              'tasks_milestone':milestone,
              'tasks_priority':priority,
              'status':status,
              'parent_id':path_id,
              'tester':tester,
              'project_id':project_id
        }
        testConnection(Conn)
        result=DB.InsertNewRecordInToTable(Conn,"tasks",**Dict)
        if result==True:
            for each in teams:
                #form new Dict
                team_dict={
                    'task_id':task_id,
                    'team_id':each
                }
                testConnection(Conn)
                result=DB.InsertNewRecordInToTable(Conn,"task_team_map",**team_dict)
                Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
                if len(Feature_Id) > 0:
                    feat_Dict={
                                   'id':task_id,
                                   'type':'TASK',
                                   'feature_id':Feature_Id[0]
                        }
                    fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                
                if result==False:
                    return False
            return task_id
        
        
        #register another path for the task to be grabbed by the requirement
        #register this task in the task_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
import datetime
def testConnection(Conn):
    if DB.IsDBConnectionGood(Conn)==False:
        time.sleep(1)
        Conn=GetConnection()
def insert_new_section(Conn,new_task_path):
    query="select max(task_path_id) from task_sections"
    testConnection(Conn)
    sequence_number=DB.GetData(Conn,query)
    if isinstance(sequence_number,list) and len(sequence_number)==1:
        if sequence_number[0] is None:
            sequence=1
        else:
            sequence=int(sequence_number[0])+1
    query="insert into task_sections(task_path_id,task_path) values('%s','%s')"%(sequence,new_task_path)
    cur=Conn.cursor()
    cur.execute(query)
    cur.close()
    Conn.commit()
    return sequence
        
def CreateNewTask(title,status,description,start_date,end_date,team_id,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements):
    try:
        Conn=GetConnection()
        query="select nextval('taskid_seq')"
        testConnection(Conn)
        task_id=DB.GetData(Conn,query)
        if isinstance(task_id,list) and len(task_id)==1:
            task_id=int(task_id[0])+1
            task_id=str('TASK-'+str(task_id))
        
        new_task_path=task_id.replace('-', '_')
        path_id=insert_new_section(Conn, new_task_path)
        """if section_path=="No_Parent":
            new_task_path=task_id.replace('-', '_')
            path_id=insert_new_section(Conn, new_task_path)
        else:
            query="select task_path_id,task_path from task_sections where task_path ~'%s'"%(section_path.replace('-', '_'))
            task_path=DB.GetData(Conn,query,False)
            if isinstance(task_path,list) and len(task_path)==1:
                path_id=task_path[0][0]
                path=task_path[0][1]
                new_task_path=path+"."+(task_id).replace('-','_')
                sequence=insert_new_section(Conn,new_task_path.strip())"""
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
              'project_id':project_id,
              'team_id':team_id
        }
        testConnection(Conn)
        result=DB.InsertNewRecordInToTable(Conn,"tasks",**Dict)
        if result==True:
            """for each in teams:
                #form new Dict
                team_dict={
                    'task_id':task_id,
                    'team_id':each
                }
                testConnection(Conn)
                result=DB.InsertNewRecordInToTable(Conn,"task_team_map",**team_dict)
                
                if result==False:
                    return False"""
                
            Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
            if len(Feature_Id) > 0:
                feat_Dict={
                               'fm_id':task_id,
                               'type':'TASK',
                               'feature_id':Feature_Id[0]
                    }
                fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                
            if labels[0] != '':
                for each in labels:
                    label_Dict={
                               'id':task_id,
                               'label_id':each.strip(),
                               'type':'TASK'
                    }
                    hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
                    
            if test_cases[0] != '':
                for each in test_cases:
                    cases_Dict={
                               'id1':task_id,
                               'id2':each.strip(),
                               'type1':'TASK',
                               'type2':'TC'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
                    
            if requirements[0] != '':
                for each in requirements:
                    req_Dict={
                               'id1':each.strip(),
                               'id2':task_id,
                               'type1':'REQ',
                               'type2':'TASK'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**req_Dict)
                    if new_result==True:
                        #t_cases = DB.GetData(Conn,"select id2 from components_map where id1='"+task_id+"' and type1='TASK' and type2='TC'",False)
                        for tc in test_cases:
                            cases_Dict={
                                       'id1':each.strip(),
                                       'id2':tc.strip(),
                                       'type1':'REQ',
                                       'type2':'TC'
                            }
                            new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
                    
            return task_id
        
        
        #register another path for the task to be grabbed by the task
        #register this task in the task_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
        
        
        
def ModifyTask(task_id,title,status,description,start_date,end_date,team_id,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements):
    try:
        Conn=GetConnection()
        
        """if section_path=="No_Parent":
            new_task_path=task_id.replace('-', '_')
            path_id=insert_new_section(Conn, new_task_path)
        else:
            query="select task_path_id,task_path from task_sections where task_path ~'%s'"%(section_path.replace('-', '_'))
            task_path=DB.GetData(Conn,query,False)
            if isinstance(task_path,list) and len(task_path)==1:
                path_id=task_path[0][0]
                path=task_path[0][1]
                new_task_path=path+"."+(task_id).replace('-','_')
                sequence=insert_new_section(Conn,new_task_path.strip())"""
        #get the current time and date
        now=datetime.datetime.now().date()
        #now form a directory to send the other information
        condition = "where tasks_id='%s'" % task_id
        Dict={
              'tasks_id':task_id,
              'tasks_title':title,
              'tasks_description':description,
              'tasks_startingdate':start_date,
              'tasks_endingdate':end_date,
              #'tasks_createdby':user_name,
              #'tasks_creationdate':now,
              'tasks_modifiedby':user_name,
              'tasks_modifydate':now,
              'tasks_milestone':milestone,
              'tasks_priority':priority,
              'status':status,
              #'parent_id':path_id,
              'tester':tester,
              'project_id':project_id,
              'team_id':team_id
        }
        testConnection(Conn)
        result=DB.UpdateRecordInTable(Conn,"tasks",condition,**Dict)
        if result==True:
            """lsres=DB.DeleteRecord(Conn,"task_team_map", task_id=task_id)
            for each in teams:
                #form new Dict
                team_dict={
                    'task_id':task_id,
                    'team_id':each
                }
                testConnection(Conn)
                result=DB.InsertNewRecordInToTable(Conn,"task_team_map",**team_dict)
                
                if result==False:
                    return False"""
                
            Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
            if len(Feature_Id) > 0:
                lsres=DB.DeleteRecord(Conn,"feature_map", fm_id=task_id)
                feat_Dict={
                               'fm_id':task_id,
                               'type':'TASK',
                               'feature_id':Feature_Id[0]
                    }
                fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                
            if labels[0] != '':
                lsres=DB.DeleteRecord(Conn,"label_map", id=task_id)
                for each in labels:
                    label_Dict={
                               'id':task_id,
                               'label_id':each.strip(),
                               'type':'TASK'
                    }
                    hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
                    
            if test_cases[0] != '':
                lsres=DB.DeleteRecord(Conn,"components_map", id1=task_id,type1='TASK',type2='TC')
                for each in test_cases:
                    cases_Dict={
                               'id1':task_id,
                               'id2':each.strip(),
                               'type1':'TASK',
                               'type2':'TC'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)      
                    
            if requirements[0] != '':
                lsres=DB.DeleteRecord(Conn,"components_map", id2=task_id,type1='REQ',type2='TASK')
                for each in requirements:
                    req_Dict={
                               'id1':each.strip(),
                               'id2':task_id,
                               'type1':'REQ',
                               'type2':'TASK'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**req_Dict)
                    if new_result==True:
                        #t_cases = DB.GetData(Conn,"select id2 from components_map where id1='"+task_id+"' and type1='TASK' and type2='TC'",False)
                        for tc in test_cases:
                            cases_Dict={
                                       'id1':each.strip(),
                                       'id2':tc.strip(),
                                       'type1':'REQ',
                                       'type2':'TC'
                            }
                            #case_exist = DB.GetData(Conn,"select count(*) from components_map where id1='"+each+" and id2'"+tc+"' and type1='REQ' and type2='TC'")
                            #if case_exist == 0:
                            new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)  
                    
            return task_id
        
        
        #register another path for the task to be grabbed by the task
        #register this task in the task_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
        
        
        
def CreateChildTask(title,status,description,start_date,end_date,team_id,tester,priority,milestone,project_id,section_path,feature_path,user_name,labels,test_cases,requirements):
    try:
        Conn=GetConnection()
        query="select nextval('taskid_seq')"
        testConnection(Conn)
        task_id=DB.GetData(Conn,query)
        if isinstance(task_id,list) and len(task_id)==1:
            task_id=int(task_id[0])+1
            task_id=str('TASK-'+str(task_id))
        
        query="select task_path_id,task_path from task_sections where task_path ~'*.%s'"%(section_path.replace('-', '_'))
        task_path=DB.GetData(Conn,query,False)
        if isinstance(task_path,list) and len(task_path)==1:
            path_id=task_path[0][0]
            path=task_path[0][1]
            new_task_path=path+"."+(task_id).replace('-','_')
            sequence=insert_new_section(Conn,new_task_path.strip())
            """if section_path=="No_Parent":
            new_task_path=task_id.replace('-', '_')
            path_id=insert_new_section(Conn, new_task_path)
        else:
            query="select task_path_id,task_path from task_sections where task_path ~'%s'"%(section_path.replace('-', '_'))
            task_path=DB.GetData(Conn,query,False)
            if isinstance(task_path,list) and len(task_path)==1:
                path_id=task_path[0][0]
                path=task_path[0][1]
                new_task_path=path+"."+(task_id).replace('-','_')
                sequence=insert_new_section(Conn,new_task_path.strip())"""
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
              'project_id':project_id,
              'team_id':team_id
        }
        testConnection(Conn)
        result=DB.InsertNewRecordInToTable(Conn,"tasks",**Dict)
        if result==True:
            """for each in teams:
                #form new Dict
                team_dict={
                    'task_id':task_id,
                    'team_id':each
                }
                testConnection(Conn)
                result=DB.InsertNewRecordInToTable(Conn,"task_team_map",**team_dict)
                
                if result==False:
                    return False"""
                
            Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
            if len(Feature_Id) > 0:
                feat_Dict={
                               'fm_id':task_id,
                               'type':'TASK',
                               'feature_id':Feature_Id[0]
                    }
                fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                
            if labels[0] != '':
                for each in labels:
                    label_Dict={
                               'id':task_id,
                               'label_id':each.strip(),
                               'type':'TASK'
                    }
                    hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
                    
            if test_cases[0] != '':
                for each in test_cases:
                    cases_Dict={
                               'id1':task_id,
                               'id2':each.strip(),
                               'type1':'TASK',
                               'type2':'TC'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
                    
            if requirements[0] != '':
                for each in requirements:
                    req_Dict={
                               'id1':each.strip(),
                               'id2':task_id,
                               'type1':'REQ',
                               'type2':'TASK'
                    }
                    new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**req_Dict)
                    if new_result==True:
                        #t_cases = DB.GetData(Conn,"select id2 from components_map where id1='"+task_id+"' and type1='TASK' and type2='TC'",False)
                        for tc in test_cases:
                            cases_Dict={
                                       'id1':each.strip(),
                                       'id2':tc.strip(),
                                       'type1':'REQ',
                                       'type2':'TC'
                            }
                            new_result=DB.InsertNewRecordInToTable(Conn,"components_map",**cases_Dict)
            
            return task_id
        
        
        #register another path for the task to be grabbed by the task
        #register this task in the task_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
        
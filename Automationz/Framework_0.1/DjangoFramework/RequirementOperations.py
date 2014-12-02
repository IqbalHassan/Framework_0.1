import DataBaseUtilities as DB
from MySite.models import GetConnection
import datetime                    
def CreateParentRequirement(title, description, project_id, team_list, start_date, end_date, priority, status, milestone, username, feature_path,labels, tasks):
    Conn=GetConnection()
    try:
        req_id=DB.GetData(Conn,"select nextval('requirementid_seq')")
        req_id=('REQ-'+str(req_id[0]))
        req_id=req_id.strip()
        #check for the occurrances
        query="select count(*) from requirements where requirement_id='%s'"%req_id
        count=DB.GetData(Conn,query)
        if isinstance(count,list) and len(count)==1 and count[0]==0:
            #start creation process
            #insert the instances in the requirement_section table
            #form the dictionary
            query="select max(requirement_path_id) from requirement_sections"
            sequence_number=DB.GetData(Conn,query)
            if isinstance(sequence_number,list) and len(sequence_number)==1:
                if sequence_number[0] is None:
                    sequence=1
                else:
                    sequence=int(sequence_number[0])+1
                cur=Conn.cursor()
                query="insert into requirement_sections(requirement_path_id,requirement_path) values(%d,'%s')"%(sequence,req_id.replace('-','_'))
                cur.execute(query)
                Conn.commit()
                cur.close()
                #now give all the thing to the requirement table
                try:
                    """query="select id from config_values where type='milestone' and value='%s'"%milestone
                    milestone=DB.GetData(Conn,query)
                    if(len(milestone)==1 and isinstance(milestone,list)):
                        milestone=milestone[0]"""
                    now=datetime.datetime.now().date()
                    start_date=start_date.split('-')
                    starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                    end_date=end_date.split('-')
                    ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                    temp_Dict={
                               'project_id':project_id.strip(),
                               'requirement_id':req_id.strip(),
                               'requirement_title':title.strip(),
                               'requirement_description':description.strip(),
                               'requirement_startingdate':starting_date,
                               'requirement_endingdate':ending_date,
                               'requirement_priority':priority.strip(),
                               'requirement_milestone':milestone,
                               'requirement_createdby':username.strip(),
                               'requirement_creationdate':now,
                               'requirement_modifiedby':username.strip(),
                               'requirement_modifydate':now,
                               'status':status.strip(),
                               'parent_requirement_id':sequence,
                        }
                    result=DB.InsertNewRecordInToTable(Conn,"requirements",**temp_Dict)
                    if result==True:
                        for each in team_list:
                            team_Dict={
                                       'requirement_id':req_id.strip(),
                                       'team_id':each.strip(),
                            }
                            result=DB.InsertNewRecordInToTable(Conn,"requirement_team_map",**team_Dict)
                            if result==False:
                                return False
                            
                        Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
                        if len(Feature_Id) > 0:
                            feat_Dict={
                                           'id':req_id,
                                           'type':'REQ',
                                           'feature_id':Feature_Id[0]
                                }
                            fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                        if labels[0] != '':
                            for each in labels:
                                label_Dict={
                                           'id':req_id,
                                           'label_id':each.strip(),
                                           'type':'REQ'
                                }
                                hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
                        if tasks[0] != '':
                            for each in tasks:
                                task_Dict={
                                           'id1':req_id,
                                           'id2':each.strip(),
                                           'type1':'REQ',
                                           'type2':'TASK'
                                }
                                hehe_result=DB.InsertNewRecordInToTable(Conn,"components_map",**task_Dict)
                        return req_id
                    else:
                        return False
                except Exception,e:
                    print "Exception: ",e 
            else:
                return False
        else:
            return False
    except Exception,e :
        print "Exception:",e
        
        
        
def EditRequirement(req_id,title, description, project_id, team_list, start_date, end_date, priority, status, milestone, username, feature_path,labels,tasks):
    Conn=GetConnection()
    try:
        now=datetime.datetime.now().date()
        start_date=start_date.split('-')
        starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
        end_date=end_date.split('-')
        ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
        condition = "where requirement_id='%s'" % req_id
        temp_Dict={
                   'project_id':project_id.strip(),
                   'requirement_id':req_id.strip(),
                   'requirement_title':title.strip(),
                   'requirement_description':description.strip(),
                   'requirement_startingdate':starting_date,
                   'requirement_endingdate':ending_date,
                   'requirement_priority':priority.strip(),
                   'requirement_milestone':milestone,
                   #'requirement_createdby':username.strip(),
                   #'requirement_creationdate':now,
                   'requirement_modifiedby':username.strip(),
                   'requirement_modifydate':now,
                   'status':status.strip(),
                   #'parent_requirement_id':sequence,
            }
        result=DB.UpdateRecordInTable(Conn,"requirements",condition,**temp_Dict)
        if result==True:
            for each in team_list:
                result=DB.DeleteRecord(Conn, "requirement_team_map", requirement_id=req_id)
                team_Dict={
                           'requirement_id':req_id.strip(),
                           'team_id':each.strip(),
                }
                result=DB.InsertNewRecordInToTable(Conn,"requirement_team_map",**team_Dict)
                if result==False:
                    return False
                
            Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
            if len(Feature_Id) > 0:
                condition = "where id='%s'" % req_id
                feat_Dict={
                               'id':req_id,
                               'type':'REQ',
                               'feature_id':Feature_Id[0]
                    }
                fresult = DB.UpdateRecordInTable(Conn,"feature_map",condition,**feat_Dict)
            if labels[0] != '': 
                result=DB.DeleteRecord(Conn, "label_map", id=req_id)
                for each in labels:
                    label_Dict={
                               'id':req_id,
                               'label_id':each.strip(),
                               'type':'REQ'
                    }
                    hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
            if tasks[0] != '':
                result = DB.DeleteRecord(Conn,"components_map",id1=req_id,type1='REQ',type2='TASK')
                for each in tasks:
                    task_Dict={
                               'id1':req_id,
                               'id2':each.strip(),
                               'type1':'REQ',
                               'type2':'TASK'
                    }
                    hehe_result=DB.InsertNewRecordInToTable(Conn,"components_map",**task_Dict)
            return req_id
        else:
            return False
    except Exception,e :
        print "Exception:",e        
        



def CreateChildRequirement(title, description, project_id, team_list, start_date, end_date, priority, status, milestone, username, feature_path,section_path,labels,tasks):
    Conn=GetConnection()
    try:
        req_id=DB.GetData(Conn,"select nextval('requirementid_seq')")
        req_id=('REQ-'+str(req_id[0]))
        req_id=req_id.strip()
        #check for the occurrances
        query="select count(*) from requirements where requirement_id='%s'"%req_id
        count=DB.GetData(Conn,query)
        #if isinstance(count,list) and len(count)==1 and count[0]==0:
            #start creation process
            #insert the instances in the requirement_section table
            #form the dictionary
        query="select requirement_path_id,requirement_path from requirement_sections where requirement_path ~'*.%s'"%(section_path.replace('-', '_'))
        requirement_path=DB.GetData(Conn,query,False)
        if isinstance(requirement_path,list) and len(requirement_path)==1:
            path_id=requirement_path[0][0]
            path=requirement_path[0][1]
            new_requirement_path=path+"."+(req_id).replace('-','_')
            query="select max(requirement_path_id) from requirement_sections"
            sequence_number=DB.GetData(Conn,query)
            if isinstance(sequence_number,list) and len(sequence_number)==1:
                if sequence_number[0] is None:
                    sequence=1
                else:
                    sequence=int(sequence_number[0])+1
                cur=Conn.cursor()
                query="insert into requirement_sections(requirement_path_id,requirement_path) values(%d,'%s')"%(sequence,new_requirement_path)
                cur.execute(query)
                Conn.commit()
                cur.close()
                #now give all the thing to the requirement table
            try:
                """query="select id from config_values where type='milestone' and value='%s'"%milestone
                milestone=DB.GetData(Conn,query)
                if(len(milestone)==1 and isinstance(milestone,list)):
                    milestone=milestone[0]"""
                now=datetime.datetime.now().date()
                start_date=start_date.split('-')
                starting_date=datetime.datetime(int(start_date[0].strip()),int(start_date[1].strip()),int(start_date[2].strip())).date()
                end_date=end_date.split('-')
                ending_date=datetime.datetime(int(end_date[0].strip()),int(end_date[1].strip()),int(end_date[2].strip())).date()
                temp_Dict={
                           'project_id':project_id.strip(),
                           'requirement_id':req_id.strip(),
                           'requirement_title':title.strip(),
                           'requirement_description':description.strip(),
                           'requirement_startingdate':starting_date,
                           'requirement_endingdate':ending_date,
                           'requirement_priority':priority.strip(),
                           'requirement_milestone':milestone,
                           'requirement_createdby':username.strip(),
                           'requirement_creationdate':now,
                           'requirement_modifiedby':username.strip(),
                           'requirement_modifydate':now,
                           'status':status.strip(),
                           'parent_requirement_id':path_id,
                    }
                result=DB.InsertNewRecordInToTable(Conn,"requirements",**temp_Dict)
                if result==True:
                    for each in team_list:
                        team_Dict={
                                   'requirement_id':req_id.strip(),
                                   'team_id':each.strip(),
                        }
                        result=DB.InsertNewRecordInToTable(Conn,"requirement_team_map",**team_Dict)
                        if result==False:
                            return False
                        
                    Feature_Id = DB.GetData(Conn, "select feature_id from product_features where feature_path = '%s'" % feature_path)
                    if len(Feature_Id) > 0:
                        feat_Dict={
                                       'id':req_id,
                                       'type':'REQ',
                                       'feature_id':Feature_Id[0]
                            }
                        fresult = DB.InsertNewRecordInToTable(Conn,"feature_map",**feat_Dict)
                    if labels[0] != '':
                        for each in labels:
                            label_Dict={
                                       'id':req_id,
                                       'label_id':each.strip(),
                                       'type':'REQ'
                            }
                            hehe_result=DB.InsertNewRecordInToTable(Conn,"label_map",**label_Dict)
                    if tasks[0] != '':
                        for each in tasks:
                            task_Dict={
                                       'id1':req_id,
                                       'id2':each.strip(),
                                       'type1':'REQ',
                                       'type2':'TASK'
                            }
                            hehe_result=DB.InsertNewRecordInToTable(Conn,"components_map",**task_Dict)
                    return req_id
            except Exception,e:
                print "Exception: ",e 
        else:
            return False
    except Exception,e :
        print "Exception:",e

        
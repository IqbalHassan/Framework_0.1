import DataBaseUtilities as DB
from MySite.models import GetConnection
import datetime                    
def CreateParentRequirement(title,description,project_id,team_list,start_date,end_date,priority,status,milestone,username):
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
                    query="select id from config_values where type='milestone' and value='%s'"%milestone
                    milestone=DB.GetData(Conn,query)
                    if(len(milestone)==1 and isinstance(milestone,list)):
                        milestone=milestone[0]
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
                               'status':status.strip()
                        }
                    result=DB.InsertNewRecordInToTable(Conn,"requirements",**temp_Dict)
                    if result==True:
                        for each in team_list:
                            team_Dict={
                                       'requirement_id':req_id.strip(),
                                       'parent_requirement_id':sequence,
                                       'team_id':each.strip(),
                            }
                            result=DB.InsertNewRecordInToTable(Conn,"requirement_team_map",**team_Dict)
                            if result==False:
                                return False
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
from MySite.models import GetConnection
import DataBaseUtilities as DB
import time
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
        
def CreateNewTask(title,status,description,start_date,end_date,teams,tester,priority,milestone,project_id,section_path):
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
            insert_new_section(Conn, new_requirement_path)
        else:
            query="select requirement_path_id,requirement_path from requirement_sections where requirement_path ~'%s'"%(section_path.replace('-', '_'))
            requirement_path=DB.GetData(Conn,query,False)
            if isinstance(requirement_path,list) and len(requirement_path)==1:
                sequence=requirement_path[0][0]
                path=requirement_path[0][1]
                new_requirement_path=path+(task_id).replace('-','_')
                insert_new_section(Conn,new_requirement_path)
        print "more thing to come"
        #register another path for the task to be grabbed by the requirement
        #register this task in the task_section so that we can get the path faster
    except Exception,e:
        print "Exception:", e
        
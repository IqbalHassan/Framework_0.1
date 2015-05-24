__author__ = 'Raju'
import Global
user='postgres'
password_user='password'
db_name='postgres'
server=Global.get_ip()
port=Global.get_port()
import DataBaseUtilities as DB
def Check_TestCase(test_case):
    test_type = [u'automated', u'manual', u'performance']
    type_selector = []
    for item in test_type:
        sQuery = "select count(*) from test_steps_list where step_id in(select step_id from test_steps where tc_id='" + test_case + "') and steptype='" + item + "'"
        conn = DB.ConnectToDataBase(db_name,user,password_user,server)
        result = DB.GetData(conn, sQuery, False)
        conn.close()
        type_selector.append(result[0])
    conn=DB.ConnectToDataBase(db_name,user,password_user,server)
    query="select tc_type from test_cases where tc_id='%s'"%(test_case.strip())
    tc_type=DB.GetData(conn,query)[0]
    conn.close()
    b = type_selector[1]
    c = type_selector[2]
    if tc_type=='Forc':
        return "Manual"
    else:
        if b[0]>0:
            return "Manual"
        else:
            if c[0]>0:
                return "Performance"
            else:
                return "Automated"

def main():
    Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
    query="select distinct tc_id from test_cases"
    test_cases_list=DB.GetData(Conn,query)
    Conn.close()
    print test_cases_list
    for test_case in test_cases_list:
        whereQuery="where tc_id='%s'"%(test_case)
        Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
        print DB.UpdateRecordInTable(Conn,"test_cases",whereQuery,test_case_type=Check_TestCase(test_case))
        Conn.close()
if __name__=="__main__":
    main()
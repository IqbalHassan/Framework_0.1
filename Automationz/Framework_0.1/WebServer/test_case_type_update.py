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
def Check_TestCaseTime(test_case):
    query="select sum(description::int) from master_data where id Ilike '%s%%' and field='estimated' and value='time'"%test_case.strip()
    Conn = DB.ConnectToDataBase(db_name,user,password_user,server)
    stepNumber = DB.GetData(Conn, query)
    Conn.close()
    return ConvertTime(stepNumber[0])

def ConvertTime(total_time):
    seconds = total_time % 60
    minuates = total_time / 60
    minuate = minuates % 60
    hour = minuates / 60
    if seconds < 10:
        seconds = ('0' + str(seconds))
    else:
        seconds = str(seconds)
    if minuate < 10:
        minuate = ('0' + str(minuate))
    else:
        minuate = str(minuate)
    if hour < 10:
        hour = ('0' + str(hour))
    else:
        hour = str(hour)
    timeformat = hour + ':' + minuate + ':' + seconds
    timeformat = timeformat.strip()
    return timeformat

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
        Conn=DB.ConnectToDataBase(db_name,user,password_user,server)
        print DB.UpdateRecordInTable(Conn,"test_cases",whereQuery,test_case_time=Check_TestCaseTime(test_case))
        Conn.close()
if __name__=="__main__":
    main()
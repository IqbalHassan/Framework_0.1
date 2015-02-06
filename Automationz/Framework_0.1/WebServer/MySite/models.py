import DataBaseUtilities as DB
import Global

# ---------------- CUSTOM CODE ---------------#
# import CommonUtil
ip = Global.get_ip(True)

def GetConnection():
    Conn = DB.ConnectToDataBase(sDbname="postgres", sUser="postgres", sPswd="password", sHost=ip)
    return Conn
def GetData(sTableName):
    Conn = GetConnection()
    Get_Data = DB.GetData(Conn, 'Select * from %s' % sTableName, False)
    Conn.close()
    return Get_Data
def GetQueryData(sQuery):
    Conn = GetConnection()
    GetQueryData  =  DB.GetData(Conn, sQuery, False)
    Conn.close()
    return GetQueryData 
def GetColumnNames(sTableName):
    Conn = GetConnection()
    ColumnNames = DB.GetData(Conn, "SELECT column_name FROM INFORMATION_SCHEMA.Columns where TABLE_NAME = '%s'" % sTableName)
    Conn.close()
    return [Col.upper() for Col in ColumnNames]

# --------------- CUSTOM CODE ---------------- #

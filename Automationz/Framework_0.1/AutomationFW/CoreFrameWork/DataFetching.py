'''
Created on Feb 9, 2015

@author: 09
'''
from CoreFrameWork import DataBaseUtilities as DBUtil
import inspect
def Get_PIM_Data_By_Id(Data_Id):
    sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name

    Data_List = []
    SQLQuery = ("select "
    " pmd.id,"
    " pmd.field,"
    " pmd.value,"
    " pmd.keyfield,"
    " pmd.ignorefield"
    " from master_data pmd"
    " where"
    " pmd.id = '%s';" % (Data_Id))
    conn=DBUtil.ConnectToDataBase()
    Data_List = DBUtil.GetData(conn, SQLQuery, False)
    Data_List = [tuple(x[1:])for x in Data_List]
    conn.close()
    AddressList = []
    for i in range(len(Data_List) - 1, -1, -1):
        eachTuple = Data_List[i]
        if eachTuple[1].startswith(Data_Id):  # or eachTuple[0] == 'Home Address' or eachTuple[0] == 'Other Address':
            if eachTuple[1] != "":
                address_find_SQLQuery = ("select "
                " pmd.field,"
                " pmd.value,"
                " pmd.keyfield,"
                " pmd.ignorefield"
                " from master_data pmd"
                " where"
                " pmd.id = '%s'"
                " ;" % (eachTuple[1]))
                conn=DBUtil.ConnectToDataBase()
                AddressData = DBUtil.GetData(conn, address_find_SQLQuery, False)
                conn.close()
            else:
                AddressData = ''
            Data_List.pop(i)
            AddressList.append((eachTuple[0], AddressData))
    for eachAddrData in AddressList:
        Data_List.append(eachAddrData)

    return Data_List

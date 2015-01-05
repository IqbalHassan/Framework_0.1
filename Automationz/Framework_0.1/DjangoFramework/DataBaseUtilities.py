# -*- coding: utf-8 -*-
"""
To Rename the Table name: Alter Table OldTableName
                          Rename To NewTableName

To Rename the column name :Alter Table tablename
                           Rename OldcolumnName To NewColumnName

To Add Forign key: Alter Table TestData
                    ADD CONSTRAINT TC_ID FOREIGN KEY (TC_ID) REFERENCES TableName(ID)
To Drop Primary key: Alter Table test_run
                     Drop Constraint TestRun_pkey
To Change the Column Data Type: Alter Table test_run
                                Alter execution_time Type VARCHAR(255)
"""

import psycopg2, inspect, sys, time
from psycopg2.extras import DictCursor

import Global


ip = Global.get_ip()

def ConnectToDataBase(sDbname="postgres", sUser="postgres", sPswd="password", sHost=ip):

    for x in range (0, 5):
            conn = False
            try:
                conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s'" % (sDbname, sUser, sPswd, sHost))
                return conn
            except Exception as e:
                print 'Unable to connect to DB: %s' % sHost
                time.sleep(1)

def CreateTable(oConn, sTableName, *sColumnNameWtihDataType):
    """
        Description: CreateTable will create table and specified columns names
        Parameters: oConn = This is database connection object created using ConnectToDataBase function
                    sTableName = This is the string table name
                    sColumnNameWtihDataType = This is the combination of column names and its data types (ColumnName DataType(Size). It could be one or more than one
        Excample: CreateTable(DBConn,"MyTableName","TC_ID INT(size)","TestStepName VARCHAR(255)

    """
    FinalString = ""
    try:
        for each_Item in sColumnNameWtihDataType:
            FinalString = FinalString + each_Item + ","
        cur = oConn.cursor()
        cur.execute("""
                    CREATE TABLE %s
                    (%s)
                """ % (sTableName, FinalString[:len(FinalString) - 1])
                )
        oConn.commit()
        return True
    except Exception, e:
        return "Error: %s" % e

def DropTable(oConn, sTableName):
    cur = oConn.cursor()
    try:
        cur.execute(
                    """DROP Table %s
                    """ % (sTableName)
                    )
        oConn.commit()
        return True
    except Exception, e:
        return "Error: %s" % e

def GetData(oConn, sQuery, bList=True, dict_cursor=False, paginate=False, **kwargs):
    '''
    If you want to paginate, set paginate=True when calling the function and also
    provide the following parameters in order for the pagination to work properly
    Arguments needed for pagination:
    @param oConn: [Connection object] The connection object
    @param sQuery: [string] The query to execute
    @param bList: [unknown] unknown
    @param dict_cursor: [bool] Enables the cursor to query with column names instead of indices
    @param paginate: [bool] Set this argument to true if you want to paginate
    @param **kwargs: [key-word arguments] Provide three named parameters:
    (page[int] - page number, page_limit[int] - items per page, order_by[string] - provide a sort order)
    
    @return: Rows [tuple] (if not requesting for pagination)
    @return: A dictionary object [rows: resultant rows, has_next: if another page is available] (if pagination requested)
    '''
    
    cur = None
    
    page = 1
    page_limit = 'ALL'
    current_page_offset = 0
    has_next = False
    order_by = ''
    
    # if the user wants the dictionary like cursor
    if dict_cursor:
        cur = oConn.cursor(cursor_factory=DictCursor)
    else:
        cur = oConn.cursor()
    
    NameList = []
    if not paginate:
        try:
            cur.execute(
                        """%s
                        """ % (sQuery)
                        )
            rows = cur.fetchall()
            if bList != True:
                return rows
            else:
                for data in range(len(rows)):
                    NameList.append((rows[data])[0])
                return NameList
        except Exception, e:
            return "Error: %s" % e
    else:
        if not kwargs:
            return "Sorry, you must supply the required arguments"
        for i in ('page', 'page_limit', 'order_by'):
            if i not in kwargs:
                return 'Sorry, you must supply a "%s" parameter for pagination' % i
            
        try:
            for key in kwargs:
                if key == 'page':
                    page = int(kwargs[key])
                elif key == 'page_limit':
                    # We'll fetch 11 items if 10 items are requested because
                    # this will help to super-efficiently check whether there
                    # is another page remaining to be queried for next page
                    page_limit = int(kwargs[key])
                elif key == 'order_by':
                    order_by = kwargs[key]
            
            if page != 1 and page_limit != 'ALL':
                current_page_offset = (page - 1) * page_limit
            
        except ValueError as e:
            return "Error: Could not cast 'page' and/or 'page_limit' to integer", e

        try:
            query = '''
            %s ORDER BY %s LIMIT %d OFFSET %d
            ''' % (sQuery, order_by, page_limit + 1, current_page_offset)
        
            cur.execute(query)
            rows = cur.fetchall()
            
            try:
                if len(rows) == page_limit + 1:
                    has_next = True
            except Exception as e:
                pass
            
            result_dict = {
                "rows": rows[0:page_limit],
                "has_next": has_next
            }
            
            return result_dict
            
        except Exception as e:
            return "Error: %s" % e


def InsertNewRecordInToTable(oConn, sTableName, **dColumnNvalues):
    ColumnName, Column, Values, ColumnValues, K, L, i = "", "", "", "", "", "", 0
    C, D = [], []
    ColumnValuesTup = ()
    cur = oConn.cursor()
    for Column, Values in dColumnNvalues.items():
        C.append(Column)
        D.append(Values)
        ColumnValues = str(D)[1:-1]
        ColumnValuesTup = ColumnValuesTup + (Values,)

    for K in C:
        i = i + 1
        if i == len(C):
            ColumnName = ColumnName + K
        else:
            ColumnName = ColumnName + K + ", "
    try:
        data = ()
        Qstr = "INSERT INTO  %s (%s) VALUES %s;" % (sTableName, ColumnName, "%s")
        cur.execute(Qstr, (ColumnValuesTup,))
        oConn.commit()
        return True
    except Exception, e:
        return "Error: %s" % e

def UpdateRecordInTable(oConn, sTableName, sWhereQuery, **dColumnNvalues):
    sModuleName = inspect.stack()[0][3] + ": Database Utilities"
    cur = oConn.cursor()
    try:
        ColumnName, Column, Values, QueryList = "", "", "", ""
        DictionLen = len(dColumnNvalues)
        ColumnValuesTup = ()
        for Column, Values in dColumnNvalues.items():
            if (DictionLen != 1):
                QueryList = Column + " = " + "%s" + " , " + QueryList
                DictionLen = DictionLen - 1
                ColumnValuesTup = (Values,) + ColumnValuesTup
            else:
                QueryList = QueryList + Column + " = " + "%s"
                ColumnValuesTup = ColumnValuesTup + (Values,)
        sQuery = """UPDATE %s
        SET %s
        %s """ % (sTableName, QueryList, sWhereQuery)
        cur.execute(sQuery, ColumnValuesTup)
        oConn.commit()
        return True
    except Exception, e:
        return "Error: %s" % e

def DeleteRecord(oConn, sTableName, **dColumnsNvalues):
    """
        Description: Function will take three arguments and will delete the record according to data
        Parameters: oConn = This is the DataBase connection
                   sTableName = This is the Table Name from which the record will be deleted. Parameter will be string
                   dColumnsNValues = This is the dictionary, the parameters will be sent as dictionary i.e ( ColumnName1 = Values1, ColumnName2 = Values2,...)
                                     Note: parameters will be without any quote
        Return:    It will return True when done or error description when failed

    """
    cur = oConn.cursor()
    Fields = []
    FinalString = ""
    try:
        if dColumnsNvalues.items() != [] :
            for each_Item in dColumnsNvalues.items():
                Fields.append("AND %s = '%s'" % (each_Item[0], each_Item[1]))

            firstfield = Fields[0].split('AND')
            Fields[0] = firstfield[1]

            for each_Item in Fields:
                FinalString = FinalString + each_Item

            cur.execute(
                    """DELETE FROM %s
                       WHERE %s
                    """ % (sTableName, FinalString)
                    )
            oConn.commit()
            return True
        else:
            return False
    except Exception, e:
        return "Error: %s" % e

def IsDBConnectionGood(oConn):
    try:
        tempnow = GetData(oConn, "Select 1")[0]
        if tempnow == 1:
            return True
        else:
            print "Connection is Bad"
            return False
    except Exception as e:
        print "DB Exception:", e
        return False

def main():

    """
    print CreateTable(DBConn,'MediaTesting','TC_ID VARCHAR(255)','TestStepName VARCHAR(255)','Commnents VARCHAR(255)')
    print InsertNewRecordInToTable(DBConn,'TCEnvironment',1000,'Outlook','PC','Win7',"",'QNX')
    print GetData(DBConn,'MediaTesting')
    print DeleteRecordInTable(DBConn, "MediaTesting", TC_ID = 1000)
    print DropTable(DBConn, "MediaTesting")

    """

if __name__ == "__main__" :

    main()
    pass

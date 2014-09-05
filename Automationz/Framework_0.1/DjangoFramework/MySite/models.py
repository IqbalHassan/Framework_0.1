


"""
Execute the SQL query directly, without using Model layer
https://docs.djangoproject.com/en/1.3/topics/db/sql/#executing-custom-sql-directly
"""



from django.db import models

import DataBaseUtilities as DB
import Global


# import CommonUtil
ip = Global.get_ip()

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

#
# print list(Reslt[0])


# print GetData("test_sets")


# class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
# class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

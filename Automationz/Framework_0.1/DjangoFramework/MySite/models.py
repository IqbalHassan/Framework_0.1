


"""
Execute the SQL query directly, without using Model layer
https://docs.djangoproject.com/en/1.3/topics/db/sql/#executing-custom-sql-directly
"""



import DataBaseUtilities as DB
#import CommonUtil


def GetConnection():
    Conn = DB.ConnectToDataBase(sDbname="postgres", sUser="postgres", sPswd="password", sHost="135.23.123.67")
    return Conn

def GetData(sTableName):
    Conn = GetConnection()
    return DB.GetData(Conn, 'Select * from %s' % sTableName, False)

def GetQueryData(sQuery):
    Conn = GetConnection()
    return DB.GetData(Conn, sQuery, False)

def GetColumnNames(sTableName):
    Conn = GetConnection()
    ColumnNames = DB.GetData(Conn, "SELECT column_name FROM INFORMATION_SCHEMA.Columns where TABLE_NAME = '%s'" % sTableName)
    return [Col.upper() for Col in ColumnNames]

#
#print list(Reslt[0])


#print GetData("test_sets")

from django.db import models

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

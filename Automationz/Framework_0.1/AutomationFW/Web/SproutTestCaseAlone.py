__author__ = 'Raju'
import sys
from Web.SproutSupport import *
def LoginTestCase():
    BrowserSelection('Firefox')
    OpenLink('https://sproutqa.sproutatwork.com')
    Login('hossain.iqbal@gmail.com','teamWork','Riz')
    Tear_Down()
def ChangingFirstName():
    BrowserSelection('Firefox')
    OpenLink('https://sproutqa.sproutatwork.com')
    Login('hossain.iqbal@gmail.com','teamWork','Riz')
    ChangeProfileDetail(firstname='Raju',lastname='Ahmed')
    Tear_Down()
def CreateNewGroup():
    BrowserSelection('Firefox')
    OpenLink('https://sproutqa.sproutatwork.com')
    Login('hossain.iqbal@gmail.com','teamWork','Raju')
    CreateGroup('New Group','This is a group creation test','Private')
    #Tear_Down()
def TestSuite():
    #LoginTestCase()
    #ChangingFirstName()
    CreateNewGroup()
def main():
    TestSuite()
if __name__=='__main__':
    main()